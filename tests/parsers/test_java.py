from parsers import java
def test_parse():
    command_response = "openjdk version \"11.0.22\" 2024-01-16\nOpenJDK Runtime Environment Temurin-11.0.22+7 (build 11.0.22+7)\nOpenJDK 64-Bit Server VM Temurin-11.0.22+7 (build 11.0.22+7, mixed mode, sharing)\n"
    parsed = java.parse(command_response)
    assert parsed == '11.0.22+7'
