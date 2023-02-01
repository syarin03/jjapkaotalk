from socket import *

sock = socket(AF_INET,SOCK_STREAM) # 클라이언트 소켓 생성

svrIP = input(('Server IP(default: 127.0.0.1):')) # 서버입력
if svrIP == '':  # 서버입력 빈칸이면 기본값
    svrIP = '127.0.0.1'

port = input(('port(default: 2500):')) #포트번호 입력
if port == '':   # 포트번호 빈칸이면 기본값
    port = 2500
else:
    port = int(port)

sock.connect((svrIP, port)) # 서버 소켓과 연결
print('Connected to ' + svrIP)

while True:
    msg = input('Sending message:')
    if not msg:
        continue

    try:    # 데이터 송신
        sock.send(msg.encode())

    except:
        print('연결 종료')
        break

    try:    # 데이터 수신
        msg = sock.recv(1024)
        if not msg:
            print('연결 종료')
            break
        print(f'Received message: {msg.decode()}')

    except:
        print('연결 종료')
        break

sock.close()
