from os import close
import socket, sys

def server(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((hostname, port))
    sock.listen(1)

    print('Listening on address:', sock.getsockname())

    while True:
        sc, addr = sock.accept()
        print("Processing 1024 bytes at a time:")
        n = 0
        while True:
            message = sc.recv(1024)
            if not message:
                break
            reply = message.decode('ascii').upper().encode('ascii')
            sc.sendall(reply)
            n += len(message)
            print("\r %d bytes processed so far ..."%(n,), end='')
            sys.stdout.flush()
        print()
        sc.close()
        print('\t socket closed.')

def client(hostname, port, bytes):
    bytes += 15
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
    message = b'capitalize this!'
    print('Sending', bytes, 'of data, in chunks of 16 bytes.')
    sent = 0
    while sent < bytes:
        sock.sendall(message)
        sent += len(message)
        print("\r sent %d bytes"%(sent,), end="")
        sys.stdout.flush()
    print()
    sock.shutdown(socket.SHUT_WR)
    print("Recieving all the data server is sending ...")
    recieved = 0
    while True:
        data = sock.recv(42)
        if not recieved:
            print('\tThe first data recieved says', repr(data))
        if not data:
            break
        recieved += len(data)
        print('\r%d bytes of data recieved ...'%(recieved,), end='')
    print()
    sock.close()

if __name__ == '__main__':
    if sys.argv[1] == 'server':
        server(sys.argv[2], int(sys.argv[3]))
    else:
        client(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))

