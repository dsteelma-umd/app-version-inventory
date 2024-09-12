# app-version-inventory

Python application for retrieving application dependency version information
from containers running in Kubernetes.

## Prerequisites

This application uses Python 3.12.

## Quick Start

1) Checkout the repository:

```zsh
$ git clone git@github.com:dsteelma-umd/application-version-inventory.git
$ cd application-version-inventory
```

2) Build the Docker image:

```zsh
$  docker build -t app-version-inventory:latest -f Dockerfile .
```

3) Switch to the Kubernetes "test" namespace:

```zsh
$ kubectl config use-context test
```

3) Run application using the "sample_manifest.yaml" file:

```zsh
$ docker run --rm -v ~/.kube:/home/app/.kube app-version-inventory:latest \
    bash -c 'app-version-inventory --namespace=test --manifest=sample_manifest.yaml'
```

**Note:** The "~/.kube" volume mount is used to provide the Kubernetes
credentials to the container.

## Development Setup - Local

```zsh
$ git clone git@github.com:dsteelma-umd/application-version-inventory.git
$ cd application-version-inventory
$ python -m venv --prompt "app-version-inventory-py$(cat .python-version)" .venv
$ source .venv/bin/activate
$ pip install -e '.[dev,test]'
```

## Usage

Run `app-version-inventory --help` for the list of supported options:

```zsh
$ app-version-inventory --help
Usage: app-version-inventory [OPTIONS]

Options:
  --namespace TEXT             The Kubernetes namespace to query  [required]
  --manifest FILE              The application version inventory manifest file
                               [required]
  --kube-config FILE           The ".kube/config" configuration directory
  --output-format [json|text]  The ".kube/config" configuration directory
  --help                       Show this message and exit.
```

### Options

#### namespace

The Kubernetes namespace to query, typically "test", "qa", or "prod".

#### manifest

The inventory manifest containing the list of applications and dependencies
to query. See "Inventory Manifest" section below.

#### kube-config (Optional)

The location of "config" file containing the credentials necessary to
communicate with Kubernetes. Defaults to `~/.kube/config`.

#### output-format (Optional)

The format of the output. Currently the following output options are available:

* text - Human-readable text output
* json - JSON output

## Inventory Manifest

The inventory manifest controls what application dependencies are queried.

See "sample_manifest.yaml" for a working example.

The general form of the manifest file is:

```yaml
application:
    name: <The name of application whose dependencies are being inventoried>
    dependencies: # A list of one (or more) dependencies to query
        - name: <The name of the dependency>
          selector: <The Kubernetes label selector for the pod>
          container: <The name of the container. Optional if there is only one container>
          parser: <(Optional) The parser to use to parse the version from the "exec" command>
          exec:
            - <List of commands to run to query the version string>
```

The manifest may contain more than one "application" stanzas, separated by
`---`.

## Parsers

Parsers are in the "parsers" module. The following parsers are available:

* apache - Parses Apache version
* identity - Returns the "exec" command output unchanged.
  This is the default parser.
* java - Parses Java version
* mysql - Parses MySQL version
* node - Parses Node version
* postgres - Parses Postgres version
* rails - Parses Ruby on Rails version
* shibboleth_sp - Parses Shibboleth SP version
* solr - Parses Solr version
* tomcat - Parses Apache Tomcat version

New parsers can simply be added to the "parsers" module, and only require the
following method:

```python
def parse(command_response: str) -> str:
    # Do whatever processing is necessary
    return str
```

## Formatters

Formatters are in the "formatters" module. The following formatters are
available:

* json - JSON formatted output
* text - returns human-readable text

New formatters can be added to the "formatters" module, and only require the
following method:

```python
def format(applications: list[Application]) -> str:
    # Do whatever processing is necessary
    return str
```

Also, the name of the formatter should be added to the Click "output-format"
argument in "src/app_version_inventory/cli.py".
