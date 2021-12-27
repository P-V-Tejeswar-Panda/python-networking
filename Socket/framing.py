import socket, struct, sys

def max_block_size(sock):
    temp = b''
    while True:
        d = sock.recv(1)
        if d.decode('ascii') == '\n':
            break
        temp += d
    return int(temp.decode('ascii'))

def recvall(sock, length):
    message = b''
    while len(message) != length:
        data = sock.recv(length-len(message))
        if not data:
            raise Exception("connection closed abruptly!")
        message += data
    return message

def getall(sock, max_len):
    blocks = []
    try:
        while True:
            len = int(recvall(sock, max_len).decode('utf-8'))
            blocks.append(recvall(sock,len))
    except Exception:
        print("Recieved all data.")
    
    print(blocks)
    return b"".join(blocks)

def frame(msg, max):
    l = 0
    r = max
    ret = []
    while l < len(msg):
        if l+r < len(msg):
            ret.append(msg[l:l+r])
            l += r
        else:
            ret.append(msg[l:len(msg)])
            l = len(msg)
    return ret

def put_all(sock, data):
    for d in data:
        sock.sendall(str(len(d)).encode('utf-8')+d)


def server():
    info = socket.getaddrinfo(None, 65432, 0, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)[0]
    print(info)
    print(info[:3])
    sock = socket.socket(info[0], info[1], info[2])
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(info[-1])
    print("Listening on: ", sock.getsockname())
    sock.listen(1)
    sc, addr = sock.accept()
    print("Got Connection from: ", sc.getpeername())
    blk_size = max_block_size(sc)
    msg = getall(sc, blk_size)
    print(msg.decode('utf-8'))
    sock.close()

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    sock.sendall('1\n'.encode('ascii'))
    msg = "Этот лес красивый, темный и глубокий, но я должен сдержать обещание и пройти много миль, прежде чем я усну.".encode('utf-8')
    put_all(sock, frame(msg, 9))
    sock.close()


if __name__ == '__main__':
    if sys.argv[1] == 'server':
        server()
    else:
        client(sys.argv[2], int(sys.argv[3]))