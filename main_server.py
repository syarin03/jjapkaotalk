import socket
import time
from _thread import *
import json
import pymysql
from datetime import datetime


client_sockets = list()

HOST = '127.0.0.1'
PORT = 9000
DB_HOST = '10.10.21.116'
DB_USER = 'talk_admin'
DB_PASSWORD = 'admin1234'


def conn_fetch():
    con = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db='talk', charset='utf8')
    cur = con.cursor()
    return cur


def conn_commit():
    con = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db='talk', charset='utf8')
    return con


def threaded(client_socket, addr):
    while True:
        try:
            data = client_socket.recv(9999)
            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break
            # print('>> Received from ' + addr[0], ':', addr[1], data.decode())
            dic_data = json.loads(data.decode())

            if dic_data['method'] == 'chat':
                print(dic_data['user_num'], dic_data['message'])
                time = datetime.now().strftime('%F %T.%f')  # DB에 넣을 시간
                dic_data['send_time'] = time[11:-10]
                sql = f"INSERT INTO chat (room_num, member_num, send_time, message) " \
                      f"VALUES ({dic_data['room_num']}, {dic_data['user_num']}, '{time}', '{dic_data['message']}')"
                with conn_commit() as con:
                    with con.cursor() as cur:
                        cur.execute(sql)
                        con.commit()
                print(sql)

            if dic_data['method'] == 'check_id':
                print(dic_data['input_id'])
                dic_data['method'] = 'check_id_result'
                sql = f"SELECT * FROM member WHERE uid = '{dic_data['input_id']}'"
                with conn_fetch() as cur:
                    cur.execute(sql)
                    result = cur.fetchall()
                    if len(result) == 0:
                        dic_data['result'] = True
                    else:
                        dic_data['result'] = False

            if dic_data['method'] == 'login':
                print(dic_data['uid'])
                dic_data['method'] = 'login_result'
                sql = f"SELECT * FROM member WHERE uid = '{dic_data['uid']}' and upw = '{dic_data['upw']}'"
                with conn_fetch() as cur:
                    cur.execute(sql)
                    result = cur.fetchall()
                    print(result)
                    if len(result) == 0:
                        dic_data['result'] = False
                    else:
                        dic_data['result'] = True
                        dic_data['login_info'] = result[0]

            if dic_data['method'] == 'registration':
                print(dic_data['uid'])
                dic_data['method'] = 'registration_result'
                sql = f"INSERT INTO member (uid, upw, uname, phone) VALUES " \
                      f"('{dic_data['uid']}', '{dic_data['upw']}', '{dic_data['uname']}', '{dic_data['phone']}')"
                print(sql)
                with conn_commit() as con:
                    with con.cursor() as cur:
                        cur.execute(sql)
                        con.commit()
                dic_data['result'] = True

            if dic_data['method'] == 'room_list':
                print(dic_data['method'])
                sql = f"SELECT * FROM room"
                print(sql)
                with conn_fetch() as cur:
                    cur.execute(sql)
                    result = cur.fetchall()
                    dic_data['method'] = 'room_list_result'
                    dic_data['result'] = result

            if dic_data['method'] == 'load_chat':
                print(dic_data['method'])
                # sql = f"SELECT * FROM chat WHERE room_num = {dic_data['room_num']}"
                sql = f"SELECT a.room_num, b.uname, a.send_time, a.message FROM chat a LEFT JOIN member b ON a.member_num = b.num WHERE room_num = {dic_data['room_num']}"

                print(sql)
                with conn_fetch() as cur:
                    cur.execute(sql)
                    result = cur.fetchall()
                    dic_data['method'] = 'load_chat_result'
                    dic_data['result'] = result

            if dic_data['method'] == 'chat':
                send_everyone(client_sockets, dic_data)
            elif dic_data['method'] == 'load_chat_result':
                send_chat_history(client_sockets, dic_data)
            else:
                send_single(client_socket, dic_data)

        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break
    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list:', len(client_sockets))

    client_socket.close()


def send_everyone(client_sockets, dic_data):
    for client in client_sockets:
        json_data = json.dumps(dic_data)
        client.sendall(json_data.encode())


def send_single(client_socket, dic_data):
    json_data = json.dumps(dic_data)
    client_socket.sendall(json_data.encode())


def send_chat_history(client_sockets, dic_data):
    result = dic_data['result']
    del dic_data['result']
    for i in result:
        for client in client_sockets:
            # dic_data['data'] = '<div style="text-align: left; vertical-align: bottom; width : 100%;"> <b style="font-size: 14px;">' + i[1] + '</b><br> <span style="font-size: 14px;color: black;">' + i[3] + '</span> <span style="font-size: 10px;color: gray;"> ' + str(i[2]) + '</span></div>'
            dic_data['data'] = [i[1], i[3], str(i[2])]
            json_data = json.dumps(dic_data)
            client.sendall(json_data.encode())
            time.sleep(0.2)


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
