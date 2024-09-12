from parsers import tomcat
def test_parse():
    command_response = "NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED\nServer version: Apache Tomcat/9.0.88\nServer built:   Apr 9 2024 13:22:30 UTC\nServer number:  9.0.88.0\nOS Name:        Linux\nOS Version:     4.18.0-553.16.1.el8_10.x86_64\nArchitecture:   amd64\nJVM Version:    11.0.22+7\nJVM Vendor:     Eclipse Adoptium\n"
    parsed = tomcat.parse(command_response)
    assert parsed == '9.0.88'
