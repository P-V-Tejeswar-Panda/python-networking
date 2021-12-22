import socket

sock = socket.socket()
host = socket.gethostname()
port = 65432
sock.connect((host, port))
print(sock.recv(1024))
sock.close()
