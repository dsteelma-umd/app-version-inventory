from parsers import node
def test_parse():
    command_response = "v18.20.2\n"
    parsed = node.parse(command_response)
    assert parsed == '18.20.2'
