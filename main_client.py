import socket
from threading import Thread
from datetime import datetime
import sys
import re
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator
import json

form_class = uic.loadUiType("main.ui")[0]


class User:
    def __init__(self, info):
        self.num = info[0]
        self.uid = info[1]
        self.upw = info[2]
        self.uname = info[3]
        self.phone = info[4]


class ThreadClass:
    def __init__(self, form, host='127.0.0.1', port=9000):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.thread_recv = Thread(target=self.recv_data, daemon=True)
        # target: 실행할 함수, daemon: 메인스레드 종료 시 같이 종료할 것인지, args: 함수에 넘겨줄 인자
        self.thread_recv.start()
        self.form = form

    def recv_data(self):
        while True:
            data = self.client_socket.recv(1024)
            dic_data = json.loads(data.decode())

            if dic_data['method'] == 'chat':
                print('user_num:', dic_data['user_num'], 'message', dic_data['message'])
                self.form.append_message(dic_data)

            if dic_data['method'] == 'check_id_result':
                print(dic_data['result'])
                if dic_data['result']:
                    self.form.label_regist_id.setText('사용 가능한 아이디입니다')
                    self.form.isIDChecked = True
                else:
                    self.form.label_regist_id.setText('이미 사용 중인 아이디입니다')
                    self.form.isIDChecked = False

            if dic_data['method'] == 'registration_result':
                print(dic_data['result'])
                if dic_data['result']:
                    self.form.stack.setCurrentWidget(self.form.stack_regist_success)
                else:
                    self.form.label_regist_id.setText('이미 사용 중인 아이디입니다')

            if dic_data['method'] == 'login_result':
                if dic_data['result']:
                    self.form.login_user = User(dic_data['login_info'])
                    self.form.stack.setCurrentWidget(self.form.stack_main)
                    self.form.label_main_name.setText(self.form.login_user.uname)
                    self.form.btn_main_to_login.setVisible(False)
                    self.form.btn_main_to_regist.setVisible(False)
                    print('uid:', self.form.login_user.uid)
                else:
                    self.form.label_login_alert.setVisible(True)

    def send_chat(self, user_num, message):
        data = {"method": 'chat', "user_num": user_num, "message": message}
        json_data = json.dumps(data)
        self.client_socket.sendall(json_data.encode())

    def send_check_id(self, input_id):
        data = {"method": 'check_id', "input_id": input_id, "result": bool()}
        print(data['method'])
        json_data = json.dumps(data)
        self.client_socket.sendall(json_data.encode())

    def send_registration(self, uid, upw, uname, phone):
        data = {"method": 'registration', "uid": uid, "upw": upw, "uname": uname, "phone": phone}
        json_data = json.dumps(data)
        self.client_socket.sendall(json_data.encode())

    def send_login(self, uid, upw):
        data = {"method": 'login', "uid": uid, "upw": upw}
        json_data = json.dumps(data)
        self.client_socket.sendall(json_data.encode())


