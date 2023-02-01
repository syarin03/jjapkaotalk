import socket
from _thread import *
import json

HOST = '127.0.0.1'
PORT = 9000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        dic_data = json.loads(data.decode())
        print('name: ' + dic_data['name'], 'message: ' + dic_data['message'])

        # print("receive:", repr(data.decode()))


start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')

while True:
    message = input('')
    if message == 'quit':
        close_data = message
        break

    data = {"name": "tester", "message": message}
    json_data = json.dumps(data)
    client_socket.sendall(json_data.encode())

    # client_socket.send(message.encode())


client_socket.close()
