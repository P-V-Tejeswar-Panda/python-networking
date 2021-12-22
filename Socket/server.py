import socket

sock = socket.socket()
host = socket.gethostname()
port = 65432

sock.bind((host, port))
