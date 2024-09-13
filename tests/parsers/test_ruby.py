from parsers import ruby
def test_parse():
    command_response = "ruby 2.7.5p203 (2021-11-24 revision f69aeb8314) [x86_64-linux]\n"
    parsed = ruby.parse(command_response)
    assert parsed == '2.7.5p203'
