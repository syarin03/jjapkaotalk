from socket import *

print('--- Socket TCP communication server ---')

serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()

print("The server is ready to receive")

connectionSocket, addr = serverSocket.accept()
print(f'--- connection start with {addr} ---')

while True:
    response = connectionSocket.recv(1024)
    print ('client <<<', response.decode('utf-8'))

    message = input('server >>> ')
    connectionSocket.send(message.encode('utf-8'))

connectionSocket.close()