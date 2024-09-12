from parsers import solr

def test_parse():
    command_response = "8.10.1\n"
    parsed = solr.parse(command_response)
    assert parsed == '8.10.1'

