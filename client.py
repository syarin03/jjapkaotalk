from socket import *

ip = "10.10.21.119"
port = 12345

clientSocket = socket(AF_INET, SOCK_STREAM)			# 소켓 생성
clientSocket.connect((ip,port))					# 서버와 연결

print("연결 확인됐습니다.")
clientSocket.send("I am a client".encode("utf-8"))		# 데이터 송신

print("메시지를 전송했습니다.")
data = clientSocket.recv(1024)					# 데이터 수신

print("받은 데이터 : ",data.decode("utf-8"))
clientSocket.close()						# 연결 종료