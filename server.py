from socket import *

host = "10.10.21.119"
port = 12345        # 임의번호

serverSocket = socket(AF_INET, SOCK_STREAM)             # 소켓 생성
serverSocket.bind((host,port))                          # 생성한 소켓에 설정한 HOST와 PORT 맵핑
serverSocket.listen(1)                                  # 맵핑된 소켓을 연결 요청 대기 상태로 전환
print("대기중입니다")

connectionSocket,addr = serverSocket.accept()           # 실제 소켓 연결 시 반환되는 실제 통신용 연결된 소켓과 연결주소 할당

print(str(addr),"에서 접속되었습니다.")                  # 연결 완료했다고 알림

data = connectionSocket.recv(1024)                      # 데이터 수신, 최대 1024
print("받은 데이터 :", data.decode("utf-8"))             # 받은 데이터 UTF-8

connectionSocket.send("I am a server".encode("utf-8"))  # 데이터 송신
print("메시지를 보냈습니다.")

serverSocket.close()                                    # 서버 닫기