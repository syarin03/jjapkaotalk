# tcpclient.py

from socket import *
import threading
import time

def send(sock):
    while True:
        sendData = input(">>>")
        clientSocket.send(sendData.encode("utf-8"))

def recv(sock):
    while True:
        data = clientSocket.recv(1024)
        print("상대방 : ", data.decode("utf-8"))

ip = "127.0.0.1"
port = 12345

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((ip,port))

print("접속 완료")

sender = threading.Thread(target=send, args=(clientSocket,))
receiver = threading.Thread(target=recv, args=(clientSocket,))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass

clientSocket.close()