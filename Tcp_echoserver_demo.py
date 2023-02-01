from socket import *

port = 2500
BUFSIZE = 1024

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('localhost', port))
sock.listen(1)
print('waiting for clients...')

c_sock, (r_host, r_port) = sock.accept()
print('Connedcte by', r_host, r_port)

while True:
    data = c_sock.recv(1024)
    if not data:
        print('데이터가 없음')
        break
    print('Received message: ', data.decode())

    c_sock.send(data)

sock.close()