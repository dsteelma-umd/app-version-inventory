from parsers import mysql

def test_parse():
    command_response = "mysql  Ver 14.14 Distrib 5.7.31, for Linux (x86_64) using  EditLine wrapper\n"
    parsed = mysql.parse(command_response)
    assert parsed == '5.7.31'
