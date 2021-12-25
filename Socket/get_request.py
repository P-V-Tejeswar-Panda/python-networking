import socket, sys

def recvall(sock, length):
    message = b""
    while len(message) < length:
        buff = sock.recv(length - len(message))
        if not buff:
            raise EOFError('Was expecting %d bytes but recieved only'
                           '%d bytes before the connection got closed!'
                           % (length, len(message)))
        message += buff
        print(buff)
    return message

def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
    sock.sendall("GET / HTTP/1.1\r\n\
Host: example.com\r\n\
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0\r\n\
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\n\
Accept-Language: en-US,en;q=0.5\r\n\
Accept-Encoding: gzip, deflate\r\n\
Connection: keep-alive\r\n".encode('ascii'))
    reply = recvall(sock, 200)
    print(reply.decode('ascii'))
    
if __name__ == '__main__':
    client(sys.argv[1], int(sys.argv[2]))
