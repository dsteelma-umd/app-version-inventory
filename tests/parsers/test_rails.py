from parsers import rails

def test_parse():
    command_response = "Rails 6.1.7.4\n"
    parsed = rails.parse(command_response)
    assert parsed == '6.1.7.4'
