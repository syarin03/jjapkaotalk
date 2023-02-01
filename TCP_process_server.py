import socket

table = {'1': 'one', '2': 'two', '3': 'three',
        '4': 'four','5': 'five', '6':'six',
         '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten'}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('localhost', 2500)
sock.bind(address)
sock.listen(1)
print('Waiting...')
c_socket, c_addr = sock.accept()
print('Connection from ', c_addr)
# print('클라이언트 소켓', c_socket)
while True:
    data = c_socket.recv(1024).decode()
    try:
        resp = table[data]  # 키값을 통해서 resp에 밸류값 저장
        # print(resp,123)
    except:
        c_socket.send('Try again'.encode())
    else:
        c_socket.send(resp.encode())    # 밸류값을 바이트로 변환하여 송신
        # print(resp)
        # print(resp.encode())