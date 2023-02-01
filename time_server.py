import socket
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # 소켓서버 열기 ipv4,tcp
address = ('localhost', 5000)
sock.bind(address)
sock.listen(5)
print('서버 열림')
# cnt = 0

while True:
    client,addr = sock.accept() # 연결 허용, 클라이언트 소켓,주소 튜플로 반환
    print('클라이언트 연결 성공')
    # cnt += 1
    # text = f'당신은 {cnt}번째 접속자 입니다'
    print('Connection requested from ', addr)
    client.send(time.ctime(time.time()).encode()) # 데이터 보내기
    # client.send(text.encode())
    client.close() # 소켓 해제