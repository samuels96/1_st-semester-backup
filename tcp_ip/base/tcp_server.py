import socket               # Import socket module
from dummy import generate
from time import sleep

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 6669                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.


try:
	while True:
		print('Waiting for a connection...')
		c, addr = s.accept()     # Establish connection with client.
		print('Got connection from', addr)
		while True:
			sleep(0.7)
			c.send(str(generate()).encode())
			# c.send(input('Send >>> ').encode())
except:
	c.close()                # Close the connection