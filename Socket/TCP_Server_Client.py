import argparse, socket, sys, time

def recvall(sock, length):
    message = b""
    while len(message) < length:
        buff = sock.recv(length - len(message))
        if not buff:
            raise EOFError('Was expecting %d bytes but recieved only'
                           '%d bytes before the connection got closed!'
                           % (length, len(message)))
        message += buff
    return message


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(5)
    print("Listening at: ", sock.getsockname())
    while True:
        sc, sockname = sock.accept()
        print("We have accepted a connection from: ", sockname)
        print("\tSocket name: ", sc.getsockname())
        print("\tSocket peer: ", sc.getpeername())
        message = recvall(sc, 16)
        print("\tIncomeing 16 octet message: ", message)
        sc.sendall(b"")
        time.sleep(2)
        sc.close()
        print("\tReply sent, Socket closed.")

def client(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((interface, port))
    print("Client has been assigned: ", sock.getsockname())
    sock.sendall(b"Hi there, server")
    reply=recvall(sock, 16)
    print("The server said: ", repr(reply))
    sock.close()

if __name__ == "__main__":
    if sys.argv[1] == 'server':
        server(sys.argv[2], int(sys.argv[3]))
    else:
        client(sys.argv[2], int(sys.argv[3]))
