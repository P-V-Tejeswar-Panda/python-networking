#

## Using "socket.getaddrinfo()"

getaddrinfo(addr, port, sock_family, sock_type, sock_proto, flags)

- addr: the address where to connect or where to bind.
    - Wildcard: None
- port: port no. like: 80, 21 etc. or 'http', 'ftp' etc.
    - Wildcard: 0
- sock_family: family of protocol to use like: AF_INET, AF_INET6, AF_BLUETOOTH, AF_UNIX, etc.
    - Wildcard: 0
- sock_type: type of socket i.e., whether the service required is flow controlled or not. Every network layer like IP, appletalk provides both types of service.Example: SOCK_DGRAM, SOCK_STREAM
    - Wildcard: 0
- sock_proto: actual protocal name like: IPPROTO_TCP for flowcontrolled and IPPROTO_UDP for flow uncontrolled.
    - Wildcard: 0
- flags: Discussed below
    - Wildcard: 0

```

AF_INET: signifies ipv4
   |
   |
   |
   |--------------------|
   |                    |
SOCK_DGRAM          SOCK_STREAM
   |                    |
   |                    |
IPPROTO_UDP         IPPROTO_TCP

```

## Using "getaddrinfo()" to get the server bind port (You act as server)

Examples:
### 1. I want to bind to all interfaces for http service give me required info:
```python
>>> socket.getaddrinfo(None, 'http', 0, 0, 0, socket.AI_PASSIVE)
[(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('0.0.0.0', 80)), (<AddressFamily.AF_INET6: 10>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('::', 80, 0, 0))]

```

- AI_PASSIVE flag means we intend to call bind() and accept() on the addresses returned.
### 2. I want to use the port for ntp on localhost
```python
>>> socket.getaddrinfo('localhost', 'ntp', 0, 0, 0, 0)
(<AddressFamily.AF_INET6: 10>, <SocketKind.SOCK_DGRAM: 2>, 17, '', ('::1', 123, 0, 0))
(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 17, '', ('127.0.0.1', 123))
```
### 3. I want to use 127.0.0.1 for ntp
```python
>>> socket.getaddrinfo('127.0.0.1', 'ntp')
[(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 17, '', ('127.0.0.1', 123))]

```

## Using getaddrinfo() for connecting to a remote host (You act as client)

Examples;
### 1. Get me IP address for google.com for http
```python
>>> socket.getaddrinfo('google.com', 'http')
(<AddressFamily.AF_INET6: 10>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('2404:6800:4009:825::200e', 80, 0, 0))
(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('142.250.183.174', 80))

```
### 2. Get me IP address for google.com for http but only IPv4
```python
>>> socket.getaddrinfo('google.com', 'http',socket.AF_INET)
[(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('142.250.183.174', 80))]

```
### 3. get me google.com ftp port
```python
>>> socket.getaddrinfo('google.com', 'ftp' ,socket.AF_INET)
[(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('142.250.183.174', 21))]
>>> socket.getaddrinfo('google.com', 'ftp' ,socket.AF_INET6)
[(<AddressFamily.AF_INET6: 10>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('2404:6800:4009:825::200e', 21, 0, 0))]

```
### 4. get me google.com https ports but only those I can connect based on whether my system is configured for only IPv4 or only IPv6
```python
>>> socket.getaddrinfo('google.com', 'https' ,0,0,0,socket.AI_ADDRCONFIG)
[(<AddressFamily.AF_INET6: 10>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('2404:6800:4009:825::200e', 443, 0, 0)),
(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('142.250.183.174', 443))]

```
- since my laptop supports both IPv4/IPv6, it returned both else, It would have returned both.

### 5. my machine supports only IPv6 and server only supports IPv4 in that case return IPv4 server address mapped as IPv6 that my system can manage
```python
>>> socket.getaddrinfo('baidu.com', 'http' ,0,0,0,0)
[(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('220.181.38.251', 80)), (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('220.181.38.148', 80))]

``` 
- As you can see baidu.com doesn't have IPv6 support. Now, Let's say my laptop doesn't support IPv4. What to do ? I can get a mapped addess:
```python
>>> socket.getaddrinfo('baidu.com', 'http' ,0,0,0,socket.AI_V4MAPPED)
[(<AddressFamily.AF_INET6: 10>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('64:ff9b::dcb5:2694', 80, 0, 0)), 
(<AddressFamily.AF_INET6: 10>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('64:ff9b::dcb5:26fb', 80, 0, 0)), 
(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('220.181.38.148', 80)), 
(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('220.181.38.251', 80))]
```