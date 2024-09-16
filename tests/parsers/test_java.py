from parsers import java

def test_parse_temurin():
    # Temurin OpenJDK response
    command_response = "openjdk version \"11.0.22\" 2024-01-16\nOpenJDK Runtime Environment Temurin-11.0.22+7 (build 11.0.22+7)\nOpenJDK 64-Bit Server VM Temurin-11.0.22+7 (build 11.0.22+7, mixed mode, sharing)\n"
    parsed = java.parse(command_response)
    assert parsed == '11.0.22+7'

def test_parse_icedtea():
    # IcedTea OpenJDK response
    command_response = "openjdk version \"1.8.0_212\"\nOpenJDK Runtime Environment (IcedTea 3.12.0) (Alpine 8.212.04-r0)\nOpenJDK 64-Bit Server VM (build 25.212-b04, mixed mode)\n"
    parsed = java.parse(command_response)
    assert parsed == '1.8.0_212'


