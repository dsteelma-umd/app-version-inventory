import re

def parse(command_response: str) -> str:
    match = re.search(r".*version: .*\/(.*)", command_response)
    if match:
        return match.group(1)
