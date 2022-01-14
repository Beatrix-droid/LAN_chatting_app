import socket
from threading import Thread

HOST = "0.0.0.0"
# must be a web server ip if run on a web server
PORT = 55008


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

# Making the port a reusable port:
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Listen for connections:
client_sockets = []
nicknames = []
# Server listening for incoming connections
s.listen()

# function that sends a message to all clients connected on the server:


def broadcast(message):
	for client in client_sockets:
		client.send(message)


def accept_clients(client):

	""" A function that listens out for messages from the client socket.
	When a message is received, it broadcasts it out to other connected clients"""

	while True:
		try:
			# try to receive a message from the client and if it succeeds broadcast it to the rest of the connected clients
			message = client.recv(1024).decode()
			broadcast(message)

		except Exception as e:
			# the client is no longer connected and must be removed. We are going to cut the connection and terminate the loop
			print(f"Error: {e}")
			# find the index this particular client has in the client_socket list so that we can remove it
			index = client_sockets.index(client)
			client_sockets.remove(client)
			client.close()

			# set the nickname index to be the same as the client index so that we can easily remove the nickname as well without
			# creating inconsistencies.
			nickname = nicknames[index]
			nicknames.remove(nickname)
			broadcast(f"{nickname} has left the chat".encode("ascii"))
			break


def receive():
	while True:
		# we will see the client and its Ip address when it connects to the server
		client, client_address = s.accept()
		print(f"{client_address} has connected")

		# prompt client to enter a nickname:
		client.send("NICK".encode("ascii"))
		nickname = client.recv(1024).decode("ascii")

		# add new connected client to the connected sockets
		nicknames.append(nickname)
		client_sockets.append(client)
		print(f"nickname of client is {nickname}.".encode("ascii"))
		broadcast(f"{nickname} has joined the chat!".encode("ascii"))
		client.send("connected to the server".encode("ascii"))

		# start a new thread that listens for each client's messages and handles them at the same time
		thread = Thread(target=accept_clients, args=(client,))
		# make the thread daemon such that it ends whenever the main thread ends
		thread.daemon = True
		thread.start()


print("server is listening...")

receive()
