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
            print('name: ' + dic_data['name'], 'message: ' + dic_data['message'])
            self.form.append_message(dic_data)
            # print("receive:", repr(data.decode()))

    def send_data(self, name, message):
        data = {"name": name, "message": message}
        json_data = json.dumps(data)
        self.client_socket.sendall(json_data.encode())
        # self.client_socket.send(message.encode())


class WindowClass(QMainWindow, form_class):
    login_user = None
    isIDChecked = False
    isPWRuleChecked = False
    isPWSameChecked = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.thread = ThreadClass(self)  # 스레드에 GUI 같이 넘겨주기

        # region 실행 시 초기 세팅
        input_rule_eng_num = QRegExp("[A-Za-z0-9]*")
        input_rule_phone = QRegExp("[0-9]{0,11}")
        self.input_login_id.setValidator(QRegExpValidator(input_rule_eng_num, self))
        self.input_login_pw.setValidator(QRegExpValidator(input_rule_eng_num, self))
        self.input_regist_id.setValidator(QRegExpValidator(input_rule_eng_num, self))
        self.input_regist_pw.setValidator(QRegExpValidator(input_rule_eng_num, self))
        self.input_regist_pwck.setValidator(QRegExpValidator(input_rule_eng_num, self))
        self.input_regist_phone.setValidator(QRegExpValidator(input_rule_phone, self))

        self.stack.setCurrentWidget(self.stack_main)
        # endregion

        # region 페이지 이동
        self.btn_main_to_login.clicked.connect(self.go_login)

        self.btn_main_to_regist.clicked.connect(self.go_regist)

        self.btn_main_to_chat.clicked.connect(self.go_chat)

        self.btn_login_to_main.clicked.connect(self.go_main)
        self.btn_regist_to_main.clicked.connect(self.go_main)
        self.btn_find_to_main.clicked.connect(self.go_main)
        # endregion

        # self.btn_test.clicked.connect(self.test)
        self.btn_send_text.clicked.connect(self.send_text)
        self.btn_login.clicked.connect(self.login)

        self.input_chat_text.textChanged.connect(self.set_enabled_send)
        self.input_chat_text.returnPressed.connect(self.send_text)

    # region 페이지 이동 함수들
    def go_main(self):
        self.stack.setCurrentWidget(self.stack_main)

    def go_login(self):
        self.stack.setCurrentWidget(self.stack_login)

    def go_regist(self):
        self.stack.setCurrentWidget(self.stack_regist)

    def go_find(self):
        self.stack.setCurrentWidget(self.stack_find)

    def go_chat(self):
        self.stack.setCurrentWidget(self.stack_room_chat)

    # endregion

    # def test(self):
    #     time = datetime.now().strftime('%F %T.%f')
    #     msg_time = datetime.now().strftime('%H:%M')
    #     print('time:', time)
    #     print('msg time:', msg_time)
    #     self.label_time.setText(time)
    #     self.label_msg_time.setText(msg_time)

    def send_text(self):
        time = datetime.now().strftime('%F %T.%f')  # DB에 넣을 시간
        msg_time = datetime.now().strftime('%H:%M')  # 출력할 시간
        chat = self.input_chat_text.text()
        self.thread.send_data('name', chat)
        # self.browser_chat.append(
        #     '<div style="text-align: right; vertical-align: bottom;">'
        #     '<span style="font-size: 10px; color: gray;">' + msg_time + '</span>'
        #     '<span style="font-size: 14px; color: black;"> ' + chat + '</span>'
        #     '</div>')
        self.input_chat_text.clear()

    def append_message(self, message):
        self.browser_chat.append(
            '<div style="text-align: right; vertical-align: bottom;">'
            # '<span style="font-size: 10px; color: gray;">' + msg_time + '</span>'
            '<span style="font-size: 14px; color: black;"> ' + message['message'] + '</span>'
                                                                                    '</div>')

    def set_enabled_send(self):
        if self.input_chat_text.text() == '':
            self.btn_send_text.setEnabled(False)
            self.btn_send_text.setStyleSheet("border-radius: 5px; background-color: #d9d9d9;")
        else:
            self.btn_send_text.setEnabled(True)
            self.btn_send_text.setStyleSheet("border-radius: 5px; background-color: #FEE500;")

    def login(self):
        print('login')
        # 서버로 넘겨주는 걸로 바꿔야 함
        # sql = f"SELECT * FROM member WHERE uid = '{self.input_login_id.text()}' and upw = '{self.input_login_pw.text()}'"
        # with conn_fetch() as cur:
        #     cur.execute(sql)
        #     result = cur.fetchall()
        #     if len(result) == 0:
        #         QMessageBox.warning(self, '경고', '아이디 또는 비밀번호가 일치하지 않습니다')
        #     else:
        #         self.login_user = User(result[0])
        #         QMessageBox.information(self, '알림', '로그인 되었습니다')
        #         self.stack.setCurrentWidget(self.stack_main)

    def logout(self):
        self.login_user = None
        QMessageBox.information(self, '알림', '로그아웃 되었습니다')

    def registration(self):
        if len(self.input_regist_id.text()) <= 0 or len(self.input_regist_pw.text()) <= 0 or len(
            self.input_regist_pwck.text()) <= 0 or len(self.input_regist_name.text()) <= 0 or len(
            self.input_regist_phone.text()) <= 0:
            QMessageBox.warning(self, '경고', '모든 입력칸을 확인해주세요')
        elif not self.isIDChecked:
            QMessageBox.warning(self, '경고', '아이디 중복 확인을 해주세요')
        elif not self.isPWRuleChecked or not self.isPWSameChecked:
            QMessageBox.warning(self, '경고', '비밀번호를 확인해주세요')
        else:
            regist_id = self.input_regist_id.text()
            regist_pw = self.input_regist_pw.text()
            regist_name = self.input_regist_name.text()
            regist_phone = self.input_regist_phone.text()
            # 서버로 넘겨주는 걸로 바꿔야함
            # sql = f"INSERT INTO member (uid, upw, uname, phone) VALUES ('{regist_id}', '{regist_pw}', '{regist_name}', '{regist_phone}')"
            # print(sql)
            # with conn_commit() as con:
            #     with con.cursor() as cur:
            #         cur.execute(sql)
            #         con.commit()
            # QMessageBox.information(self, '알림', '회원가입에 성공하였습니다')
            # self.stackedWidget.setCurrentWidget(self.stack_main)

    def id_changed(self):
        self.isIDChecked = False
        self.btn_regist_idck.setEnabled(True)

    def pw_changed(self):
        if self.input_regist_pw.text().isdigit() or self.input_regist_pw.text().isalpha() or len(
                self.input_regist_pw.text()) < 8:
            self.label_pw_rule.setText('영문 숫자 혼용하여 8글자 이상이어야 합니다')
            self.isPWRuleChecked = False
        else:
            self.label_pw_rule.clear()
            self.isPWRuleChecked = True
        if self.input_regist_pw.text() != self.input_regist_pwck.text():
            self.label_pw_check.setText('비밀번호가 일치하지 않습니다')
            self.isPWSameChecked = False
        else:
            self.label_pw_check.clear()
            self.isPWSameChecked = True

    def check_id(self):
        print('check_id')
        # 서버로 넘겨주는 걸로 바꿔야 함
        # sql = f"SELECT * FROM member WHERE uid = '{self.input_regist_id.text()}'"
        # with conn_fetch() as cur:
        #     cur.execute(sql)
        #     result = cur.fetchall()
        #     if len(result) == 0:
        #         self.isIDChecked = True
        #         QMessageBox.information(self, '알림', '사용 가능한 아이디입니다')
        #         self.btn_regist_idck.setEnabled(False)
        #     else:
        #         self.isIDChecked = False
        #         QMessageBox.warning(self, '경고', '이미 사용 중인 아이디입니다')
        #         self.btn_regist_idck.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
