# from dataclasses import dataclass
import click
from importlib import import_module
from kubernetes import client, config
from kubernetes.stream import stream
from pkgutil import iter_modules
import formatters
import parsers
import yaml
from app_version_inventory.core.application import Application
from app_version_inventory.core.dependency import Dependency

# @dataclass
# class Application:
#     name: str
#     dependencies: list[str]

# @dataclass
# class Dependency:
#     name: str
#     version: str

def load_formatters():
    # load all defined formatters from the app_version_inventor.formatters
    # package, using introspection
    formatter_modules = {}
    for finder, name, ispkg in iter_modules(formatters.__path__):
        module_name = name
        # if module_name == "importcommand":
        #     # Special case handling for "importcommand", because "import" is
        #     # a Python reserved word that is not usable as a module name,
        #     # while we want "import" to be the Plastron command
        #     name = "import"

        module = import_module(formatters.__name__ + '.' + module_name)
        formatter_modules[name] = module

        # if hasattr(module, 'configure_cli'):
        #     module.configure_cli(subparsers)
        #     command_modules[name] = module
    return formatter_modules


def load_parsers():
    # load all defined parsers from the app_version_inventor.parsers package,
    # using introspection
    parser_modules = {}
    for finder, name, ispkg in iter_modules(parsers.__path__):
        module_name = name
        # if module_name == "importcommand":
        #     # Special case handling for "importcommand", because "import" is
        #     # a Python reserved word that is not usable as a module name,
        #     # while we want "import" to be the Plastron command
        #     name = "import"

        module = import_module(parsers.__name__ + '.' + module_name)
        parser_modules[name] = module

        # if hasattr(module, 'configure_cli'):
        #     module.configure_cli(subparsers)
        #     command_modules[name] = module
    return parser_modules

@click.command()
@click.option('--namespace',
              required=True,
              help='The Kubernetes namespace to query')
@click.option('--manifest',
              required=True,
              type=click.Path(
                  exists=True,
                  file_okay=True,
                  dir_okay=False,
              ),
              help='The application version inventory manifest file')
@click.option('--kube-config',
              default=None,
              type=click.Path(
                  exists=True,
                  file_okay=True,
                  dir_okay=False
              ),
              help='The ".kube/config" configuration directory')
@click.option('--output-format',
              default='json',
              type=click.Choice(
                   ['json', 'text'],
                   case_sensitive=False),
              help='The ".kube/config" configuration directory')
def main(namespace: str, manifest: str, kube_config: str, output_format):

    # -------------

    # Configs can be set in Configuration class directly or using helper utility
    if kube_config:
      config.load_kube_config(config_file=kube_config)
    else:
        config.load_kube_config()

    v1 = client.CoreV1Api()

#    namespace = "test"

    formatter_modules = load_formatters()
    parser_modules = load_parsers()

    manifest_filename = manifest
    # ---------------

    with open(manifest_filename, 'r') as file:
        manifests = yaml.safe_load_all(file)

        applications = []
        for manifest in manifests:
            # print(f"Name: {manifest['application']['name']}")
            dependencies = manifest['application']['dependencies']
            application = Application(name=manifest['application']['name'], dependencies=[])
            applications.append(application)

            for dependency in dependencies:
                dependency_name = dependency['name']
                pod_selector = dependency['selector']
                container = dependency.get('container', None)
                parser_name = dependency.get('parser', 'identity')
                exec_cmd = dependency['exec']
                # print(f"\t{dependency_name}")
                # print(f"\t\t{pod_selector}")
                # print(f"\t\t{exec_cmd}")


                ret = v1.list_namespaced_pod(namespace=namespace, label_selector=pod_selector)
                pods = ret.items
                if pods:
                  first_pod = ret.items[0]
                  pod_name = first_pod.metadata.name
                  # print(f"Pod Name: {pod_name}")

                  resp = stream(v1.connect_get_namespaced_pod_exec,
                                  pod_name,
                                  namespace,
                                  container=container,
                                  command=exec_cmd,
                                  stderr=True, stdin=False,
                                  stdout=True, tty=False)
                  parsed_response = resp
                  parser_module = parser_modules[parser_name]
                  parsed_response = parser_module.parse(resp)

                  dependency = Dependency(name=dependency_name, version=parsed_response)
                  application.dependencies.append(dependency)
                  # print(f"Response: {dependency}")

    # print("============")
    # print(f"applications: {applications}")
    # print("============")
    # formatter_name = "text"
    # formatter_module = formatter_modules[formatter_name]
    # print(formatter_module.format(applications))
    # print("============")
    # formatter_name = "json"
    # formatter_module = formatter_modules[formatter_name]
    # print(formatter_module.format(applications))

    formatter_module = formatter_modules[output_format]
    print(formatter_module.format(applications))