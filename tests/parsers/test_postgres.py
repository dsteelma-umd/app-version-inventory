from parsers import postgres
def test_parse():
    command_response = "psql (PostgreSQL) 13.10 (Debian 13.10-1.pgdg110+1)\n"
    parsed = postgres.parse(command_response)
    assert parsed == '13.10'

    command_response = "psql (PostgreSQL) 9.5.16"
    parsed = postgres.parse(command_response)
    assert parsed == '9.5.16'

