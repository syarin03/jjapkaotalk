import socket
from _thread import *
import json

client_sockets = list()

HOST = '127.0.0.1'
PORT = 9000


def threaded(client_socket, addr):
    # print('>> Connected by :', addr[0], ':', addr[1])

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break
            # print('>> Received from ' + addr[0], ':', addr[1], data.decode())
            dic_data = json.loads(data.decode())
            print('name: ' + dic_data['name'], 'message: ' + dic_data['message'])
            for client in client_sockets:
                # if client != client_socket:
                client.send(data)
        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break
    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))

    client_socket.close()


print('>> Server Start')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

try:
    while True:
        print('>> Wait')

        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))
        print("참가자 수 : ", len(client_sockets))

except Exception as e:
    print('에러는? : ', e)

finally:
    server_socket.close()
