import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = str(sys.argv[1])
PORT = 5008

server.connect(IP_address, PORT)

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
			sys.stdout.write("You")
			sys.stdout.write(message)
			sys.stdout.flush()
	server.close()