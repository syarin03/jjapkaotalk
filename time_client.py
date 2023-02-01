import socket

ip = 'localhost'
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, port)) # 서버로 연결 요청
print('서버에 연결 요청')
print('연결됨')
# print('현재시각: ',sock.recv(1024).decode())
# print(sock.recv(1024).decode())
sock.close()