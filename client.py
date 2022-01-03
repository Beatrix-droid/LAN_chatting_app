import socket
import select
from threading import Thread
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

PORT = 55008
client.connect((IP_address, PORT))

nickname = input("choose a nickname")


def listen_for_messages():
	while True:
		# either the server wants to send a message to be printed on the screen
		# or the client wants to give manual input to send to other people
		# maintains lists of possible input streams
		sockets_lists = [sys.stdin, client]

		read_sockets, write_socket, error_socket = select.select(sockets_lists, [], [])
		# receiving messages from the server
		for socks in read_sockets:
			try:
				message = socks.recieve(1024).decode("ascii")
				if message == "NICK":
					client.send(nickname.encode("ascii"))
				else:
					print(message)
			except:
				# if an error has occurred we close the connection
				print("An Error has occurred!")
				client.close()
				break


def write_messages():
	while True:
		message = f"{nickname}: {input('What say you?')}"
		client.send(message.encode("ascii"))


# daemon thread that listens for messages to this client and prints them
listening_thread = Thread(target=listen_for_messages())

# thread daemon must end when main thread ends
listening_thread.daemon = True
listening_thread.start()

# daemon thread that listens for messages to this client and prints them
writing_thread = Thread(target=write_messages())

# thread daemon must end when main thread ends
writing_thread.daemon = True
writing_thread.start()
