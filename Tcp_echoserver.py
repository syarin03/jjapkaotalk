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
    try:
        data = c_sock.recv(1024)
        if not data:
            c_sock.close()
            print('데이터가 없음')
            break
    except:
        print('연결 종료')
        c_sock.close()
        break
    else:
        print(data.decode())
    try:
        c_sock.send(data)
    except:
        print('연결 종료')
        c_sock.close()
        break
