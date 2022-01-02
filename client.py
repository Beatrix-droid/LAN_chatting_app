import socket
import select
import sys
from threading import Thread
#from flask import request

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = str(sys.argv[1])
PORT = 5008

server.connect(IP_address, PORT)

def listen_for_messages():
	while True:
		#maintains lists of possible input streams
		sockets_lists = [sys.stdin, server]

		#either the server wants to send a message to be printed on the screen
		#or the client wants to give manual input to send to other people

		read_sockets,write_socket, error_socket = select.select(sockets_lists,[],[])

		for socks in read_sockets:
			if socks == server:
				message = socks.recieve(1024)
				print(message)
			else:
				message = sys.stdin.readline()
				server.send(message)
				sys.stdout.write(request.form.get("username"))
				sys.stdout.write(message)
				sys.stdout.flush()

#daemon thread that listens for messages to this client and prints them
thread = Thread(target=listen_for_messages())

#thread deamon must end when main thread ends
thread.daemon = True
#start thread
thread.start()

server.close()