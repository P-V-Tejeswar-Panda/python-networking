import sys, socket, time, struct

header_struct = struct.Struct("!I")


def recv_all(sock, length):
    msg = b''
    data_len = length
    while length:
        data = sock.recv(length)
        if not data:
            raise EOFError(f"connection terminated after {len(msg)} bytes. Expected {data_len} bytes")
        msg += data
        length -= len(data)
    return msg

def send_file_name(sock, file):
    sock.sendall(header_struct.pack(len(file)))
    sock.sendall(file.encode('ascii'))


def get_file(sock, file):
    with open(file.split('/')[-1], 'w+b') as fd:
        total = 0
        while True:
            data_len = 0
            try:
                (data_len,) = header_struct.unpack(recv_all(sock, header_struct.size))
            except EOFError:
                break
            msg = recv_all(sock, data_len)
            total += len(msg)
            fd.write(msg)
            print(f'\rRecieved {total/1024} KBs', end=" ")
        print('\n Recieved the complete file.')
        


def client(host, port, file):
    sock = socket.socket()
    sock.connect((host, port))
    send_file_name(sock, file)
    sock.shutdown(socket.SHUT_WR)
    get_file(sock, file)
    sock.close()

if __name__ == "__main__":
    client(sys.argv[1], int(sys.argv[2]), sys.argv[3])


# file: /home/pvtejeswarpanda/Downloads/boat-wallpaper.jpg