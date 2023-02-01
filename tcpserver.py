#tcpserver.py

from socket import *
import threading
import time

def send(sock):                 # 데이터 송신 함수
    while True:
        sendData = input(">>>")
        sock.send(sendData.encode("utf-8"))

def recv(sock):                 # 데이터 수신 함수
    while True:
        data = connectionSocket.recv(1024)
        print("상대방 ", data.decode("utf-8"))

host = "127.0.0.1"
port = 12345

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host,port))
serverSocket.listen(1)
print("대기중입니다")

connectionSocket,addr = serverSocket.accept()

print(str(addr),"에서 접속되었습니다.")

sender = threading.Thread(target=send, args=(connectionSocket,))            # 송신 쓰레드
receiever = threading.Thread(target=recv, args=(connectionSocket,))         # 수신 쓰레드

sender.start()
receiever.start()

while True:
    time.sleep(1)   # thread 간의 우선순위 관계 없이 다른 thread에게 cpu를 넘겨줌
    pass            # sleep(0)은 cpu 선점권을 풀지 않음

serverSocket.close()                                    # 서버 닫기
