from parsers import apache

def test_parse():
    command_response = "Server version: Apache/2.4.57 (Unix)\nServer built:   Jun 13 2023 06:36:54\n"
    parsed = apache.parse(command_response)
    assert parsed == '2.4.57'
