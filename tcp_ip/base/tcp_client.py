import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 6669         # Reserve a port for your service.


try:
	s.connect((host, port))
	print('Connected to', host)
	print('\nListening for traffic...')
	while True:
		print(s.recv(1024).decode())
except:
	print('Connection to the server failed.')
	s.close                     # Close the socket when done
	