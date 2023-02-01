import socket

sock = socket.create_connection(('localhost', 2500))

message = '클라이언트 메세지'
print(f'sending {message}')
sock.sendall(message.encode())

data = sock.recv(1024)
# print('received {data.decode()}')
print('received {}'.format(data.decode()))
# print('received {}'.format(data))
print('closing socket')
sock.close()
