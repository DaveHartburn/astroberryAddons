# Network comms test - server
# Very basic communication to a client

import socket

port = 3002     # A port to run the server on

print("Server starting......")
# Create a socket to listen on
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind to the hostname
s.bind(('', port))
# Start listening
s.listen(5)

while True:
    # accept connections from outside
    (clientsocket, address) = s.accept()
    print("New connection from ", address)
    # Send a hello over the connection
    msg = "Hello remote client\n"
    clientsocket.send(msg.encode('ascii'))
    # Receive data from the client
    (bbuffer, raddr) = clientsocket.recvfrom(1024)
    print("Message from", raddr)
    print("Message: ", bbuffer)
