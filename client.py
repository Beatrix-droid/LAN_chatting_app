import socket
import select
import sys
from threading import Thread


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = str(sys.argv[1])
PORT = 55008
client.connect((IP_address, PORT))

nickname = input("choose a nickname")

def listen_for_messages():
	while True:
		# either the server wants to send a message to be printed on the screen
		# or the client wants to give manual input to send to other people
		# maintains lists of possible input streams
		sockets_lists = [sys.stdin, client]


		read_sockets,write_socket, error_socket = select.select(sockets_lists,[],[])
		# receiving messages from the server
		for socks in read_sockets:
			try:
				message = socks.recieve(1024).decode("ascii")
				if message == "NICK":
					client.send(nickname.encode("ascii"))
				else:
					print(message)
			except:
				# if an error has occured we close the connection
				print("An Error has occurred!")
				client.close()
				break


			# daemon thread that listens for messages to this client and prints them
			thread = Thread(target=listen_for_messages())

			# thread deamon must end when main thread ends
			thread.daemon = True
			# start thread
			thread.start()

