import socket

sock = socket.socket()
host = socket.gethostname()
port = 65432

sock.bind((host, port))
sock.listen(5)

while True:
    connection, addr = sock.accept()
    print("Got a connection form: ", addr)
    connection.send(b"Thank you for connecting!")
    connection.close()
    
