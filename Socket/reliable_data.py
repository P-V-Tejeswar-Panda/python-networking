# aims to provide a reliable data interchange and also support multiformat encoding

'''
step - 1. Encode the data
step - 2. Break into variable length blocks
for each block:
    step - 3. pack and send the length of each block using struct
    step - 4. send data block
'''

import socket, sys, struct, random

MSG = "Этот лес красивый, темный и глубокий, но я должен сдержать обещание и пройти много миль, прежде чем я усну."
def recvall(sock, length):
    message = b''
    while len(message) != length:
        data = sock.recv(length-len(message))
        if not data:
            raise EOFError("connection closed abruptly!")
        message += data
    return message

def frame(msg):
    l = 0
    ret = []
    while l < len(msg):
        r = random.randint(5,9)
        if l+r < len(msg):
            ret.append(msg[l:l+r])
            l += r
        else:
            ret.append(msg[l:len(msg)])
            l = len(msg)
    return ret

def put_msg(sock, msg):
    struct_header = struct.Struct('!I')
    blocks = frame(msg)
    for data in blocks:
        sock.sendall(struct_header.pack(len(data)))
        sock.sendall(data)

def get_msg(sock):
    struct_header = struct.Struct('!I')
    blocks = []
    while True:
        block_len = 0
        try:
            block_len = recvall(sock, struct_header.size)
        except EOFError as err:
            break
        (b_len,) = struct_header.unpack(block_len)
        blocks.append(recvall(sock, b_len))
    #print(blocks)
    return b''.join(blocks)

def server():
    info = socket.getaddrinfo(None, 65432, 0, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)[0]
    sock = socket.socket(info[0], info[1], info[2])
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(info[-1])
    sock.listen(1)
    print("Listening on:",sock.getsockname())
    sc, _ = sock.accept()
    print("Got connection from:", sc.getpeername())
    data = get_msg(sc)
    msg = data.decode('utf-8')
    print(data.decode('utf-8'))
    if msg == MSG:
        print("Integrity maintained!")
    else:
        print("Failed to maintain integrity.")
    sc.close()

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    msg = MSG.encode('utf-8')
    put_msg(sock, msg)
    sock.close()

if __name__ == "__main__":
    if sys.argv[1] == 'server':
        server()
    else:
        client(sys.argv[2], int(sys.argv[3]))
