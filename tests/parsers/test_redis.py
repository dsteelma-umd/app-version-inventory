from parsers import redis

def test_parse():
    command_response = "Redis server v=7.0.5 sha=00000000:0 malloc=jemalloc-5.2.1 bits=64 build=8fdc9f58f913def3\n"
    parsed = redis.parse(command_response)
    assert parsed == '7.0.5'
