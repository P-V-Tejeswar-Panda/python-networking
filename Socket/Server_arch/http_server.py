import socket, sys
import concurrent.futures

def parse_http(sock):
    request_URL = ""
    method = ""
    http_version = ""
    body = ''
    headers = {}
    head = b''
    while b"\r\n\r\n" not in head:
        head += sock.recv(1)
    head = head[:-4]
    print(head)
    parts = head.split(b'\r\n')
    method, request_URL, http_version = parts[0].split(b" ")
    print("\n\n",method, request_URL, http_version)
    print(parts)
    for i in range(1, len(parts)):
        print(parts[i].split(b':'))
        tmp = parts[i].split(b":")
        key = tmp[0]
        value = tmp[1]
        headers[key] = value
    bd = b''
    if method == b"GET":
        return method, request_URL, http_version, headers, body 

    while b"\r\n" not in bd:
        data = sock.recv(1)
        if not data:
            break
        bd += data
    bd.replace(b"\r\n", b"")
    body = bd.decode('utf-8')
    return method, request_URL, http_version, headers, body 

def build_response(http_version, respose_code, response, headers, body):
    reply = b''
    reply += b"%s %s %s\r\n" % (http_version, respose_code, response)
    for key in headers.keys():
        reply += b'%s:%s\r\n' % (key,headers[key])
    reply += b'\r\n'
    reply += body.encode('utf-8')
    reply += b'\r\n'

    return reply



def service_agent(args):
    sock = args[0]
    id   = args[1]
    print(f"Service Agent#{id} Ready ...")
    while True:
        sc, _ = sock.accept()
        print(f"Service Agent#{id} got connection from: {sc.getpeername()}")
        print(parse_http(sc))
        ver = b'HTTP/1.1'
        code = b'200'
        msg = b'OK'
        body = '<h1>Hello World!</h1>'
        dict = {}
        dict[b'Date']=b'Sat, 09 Oct 2010 14:28:02 GMT'
        dict[b'Server']=b'Apache'
        dict[b'Last-Modified']=b'Tue, 01 Dec 2009 20:18:22 GMT'
        dict[b'Accept-Ranges']=b'bytes'
        dict[b'Content-Length']=b'%d'%(len(body.encode('utf-8'))+2)
        dict[b'Content-Type']=b'text/html'
        
        response = build_response(ver, code, msg, dict, body)
        print("Response:\n\n", response.decode('ascii'))
        sc.sendall(response)
        sc.close()





def server(host, port, worker, worker_count):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(worker_count)
    print("Listening on:", sock.getsockname())
    with concurrent.futures.ThreadPoolExecutor() as Executor:
        worker_pool = Executor.map(worker, [(sock, id) for id in range(worker_count)])
        for worker in worker_pool:
            print(worker)
    sock.close()


if __name__ == '__main__':
    server('0.0.0.0', 65432, worker=service_agent, worker_count=3)