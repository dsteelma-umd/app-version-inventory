from app_version_inventory.core.application import Application
from app_version_inventory.core.dependency import Dependency

def format(applications: list[Application]):
    return format_applications(applications)

def format_applications(applications: list[Application]) -> str:
    str =""
    for application in applications:
        str += f"{format_application(application)}\n"
        str += "------------"
    return str

def format_application(application: Application) -> str:
    str = ""
    for dependency in application.dependencies:
        str += f"{format_dependency(dependency)}\n"
    return str

def format_dependency(dependency: Dependency) -> str:
    return f"{dependency.name}: {dependency.version}"

