import socket, sys, struct, time
import concurrent.futures

header_struct = struct.Struct("!I")

'''
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
'''
def recv_all(sock, length):
    message = b''
    while len(message) != length:
        data = sock.recv(length-len(message))
        if not data:
            raise EOFError("connection closed abruptly!")
        message += data
    return message

def send_all(sock, file, ID):
    with open(file, 'r+b') as fd:
        sent_bytes = 0
        while True:
            block = fd.read(4096)
            if len(block) != 0:
                sent_bytes += len(block)
                sock.sendall(header_struct.pack(len(block)))
                sock.sendall(block)
                print(f"\rService Agent#{ID}: Sent {sent_bytes/1024} KBs.", end=" ")
                time.sleep(0.05)
            else:
                print("\t-\tComplete.")
                break

def service_agent(arg):
    sock = arg[0]
    ID = arg[1]
    print(f"Service Agent#{ID} Ready ...")
    while True:
        sc, _ = sock.accept()
        print(f"Service Agent#{ID} got connection from: {sc.getpeername()}")
        (data_len,) = header_struct.unpack(recv_all(sc, header_struct.size))
        msg = recv_all(sc, data_len).decode('ascii')
        sc.shutdown(socket.SHUT_RD)
        print(f"Service Agent#{ID}: Client Requested: {msg}")
        send_all(sc, msg, ID)
        sc.shutdown(socket.SHUT_WR)
        sc.close()



def server():
    info = socket.getaddrinfo(None, 65432, 0, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)[0]
    sock = socket.socket(info[0], info[1], info[2])
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(info[-1])
    sock.listen(10)
    print("Listening on:", sock.getsockname())
    with concurrent.futures.ThreadPoolExecutor() as Executor:
        worker_pool = Executor.map(service_agent, [(sock, ID) for ID in range(10)])
        for worker in worker_pool:
            print(worker)
    sock.close()



if __name__ == '__main__':
    server()