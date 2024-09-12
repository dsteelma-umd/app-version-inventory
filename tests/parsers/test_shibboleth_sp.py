from parsers import shibboleth_sp
def test_parse():
    command_response = "'shibboleth 3.2.2\n'"
    parsed = shibboleth_sp.parse(command_response)
    assert parsed == '3.2.2'
