import socket

print(socket.gethostbyname_ex(socket.gethostname()))
FIND_IP = socket.gethostbyname_ex(socket.gethostname())

print(FIND_IP[2])




IP_address = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
print(IP_address)
