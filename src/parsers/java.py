import re

def parse(command_response: str) -> str:
    if "IcedTea" in command_response:
        match = re.search(r"openjdk version \"(.*)\"", command_response)
    else:
        # Temurin version strings
        match = re.search(r".*?\(build (.*?)\).*", command_response)

    if match:
        return match.group(1)
