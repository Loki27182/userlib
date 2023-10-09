from pynqcom import LINK

connection = LINK()

connection.send_string("Hello Dave!")
print(connection.receive_string() )

del connection
