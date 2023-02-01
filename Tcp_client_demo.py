import socket

port = 2500
address = ('localhost', port)
BUFSIZE = 1024

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.bind((address))
s.connect(address)
print('서버 연결 성공')

while True:
    msg = input('message to send: ')
    s.send(msg.encode())
    r_msg = s.recv(BUFSIZE)
    if not r_msg:break
    print('Received message: %s' %r_msg.decode())

