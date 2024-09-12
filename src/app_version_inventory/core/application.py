from dataclasses import dataclass

@dataclass
class Application:
    name: str
    dependencies: list[str]
