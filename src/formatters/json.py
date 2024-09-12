import dataclasses
import json

from app_version_inventory.core.application import Application

# From https://stackoverflow.com/a/51286749
class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

def format(applications: list[Application]):
    return json.dumps(applications, cls=EnhancedJSONEncoder, indent=4)
