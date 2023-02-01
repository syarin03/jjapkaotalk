import socket

table = {'홍길동': 20150001,'심순애': 20150002, '박문수': 20150003}

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
address =('localhost',2500)
sock.bind(address)
sock.listen(1)
print('waiting...')
c_socket, c_addr = sock.accept()
print('Connected from ',c_addr)

while True:
    data = c_socket.recv(1024).decode()
    try:
        resp = table[data]
    except:
        c_socket.send('이름이 없습니다'.encode())
        break
    else:
        c_socket.send(str(resp).encode())

