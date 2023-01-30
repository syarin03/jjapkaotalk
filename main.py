from datetime import datetime
import sys
import re
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator
import pymysql

form_class = uic.loadUiType("main.ui")[0]
HOST = '10.10.21.116'
USER = 'talk_admin'
PASSWORD = 'admin1234'


def conn_fetch():
    con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db='talk', charset='utf8')
    cur = con.cursor()
    return cur


def conn_commit():
    con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db='talk', charset='utf8')
    return con


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        input_rule_eng_num = QRegExp("[A-Za-z0-9]*")
        input_rule_num = QRegExp("[0-9]{0,11}")
        self.edit_login_id.setValidator(QRegExpValidator(input_rule_eng_num, self))
        self.edit_login_pw.setValidator(QRegExpValidator(input_rule_eng_num, self))
        # self.edit_regist_id.setValidator(QRegExpValidator(input_rule_eng_num, self))
        # self.edit_regist_pw.setValidator(QRegExpValidator(input_rule_eng_num, self))
        # self.edit_regist_pwck.setValidator(QRegExpValidator(input_rule_eng_num, self))

        self.btn_test.clicked.connect(self.test)
        time = datetime.utcnow().strftime('%F %T.%f')
        print(time)
        sql = f"INSERT INTO chat (room_num, member_num, send_time, message) VALUES (1, 1, '{time}', '')"
        with conn_commit() as con:
            with con.cursor() as cur:
                cur.execute(sql)
                con.commit()

    def test(self):
        sql = "SELECT * FROM joining"
        print(sql)
        with conn_fetch() as cur:
            cur.execute(sql)
            result = cur.fetchall()
            print(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

