from parsers import python

def test_parse():
    command_response = "Python 3.11.2\n"
    parsed = python.parse(command_response)
    assert parsed == '3.11.2'
