from socket import *

print('--- Socket TCP communication client ---')

serverName = '127.0.0.1'
serverPort = int(input('enter the server port number : '))

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

print(f'--- connected with server {serverName}:{serverPort} ---')
while True:
    message = input('client >>> ')
    clientSocket.send(message.encode('utf-8'))
    response = clientSocket.recv(1024)
    print ('server <<<', response.decode('utf-8'))

clientSocket.close()