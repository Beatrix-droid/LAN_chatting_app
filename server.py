import socket
from threading import Thread

HOST = "0.0.0.0"
PORT = 5008


s = socket.socket()
s.bind(HOST, PORT)

#Making the port a reusable port:
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

#Listen for connetctions:
client_sockets =[]
s.listen(10)

print(f"listening as {HOST}: {PORT}")


def accept_clients(client):

	""" A function that listens out for messages from the client socket.
	When a message is recieved, it broadcasts it out to other connected clients"""

	while True:
		try:
			message = client.recv(1024).decode()
		except Exception as e:
			# the client is no longer connected and must be removed
			print(f"Error: {e}")
			client_sockets.remove(client)

		for client_socket in client_sockets:
			client_socket.send(message.encode())

while True:
	# keep listening for new connections all the time
	client_socket, client_address = s.accept()
	print(f"{client_address} has conneccted")

	#add new connected client to the connected sockets
	client_sockets.append(client_socket)
	#start a new thread that listens for each client's messages

	thread = Thread (target=accept_clients, args=(client_socket,))
	#make the thread daemon so it ends whenever the main thread ends
	thread.daemon = True


#close client sockets
for client_socket in client_sockets:
	client_socket.close()

#close server socket:
s.close

