# gui 채팅 클라이언트
from socket import *
from threading import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
form_class = uic.loadUiType('./fa.ui')[0]

class Main(QMainWindow, form_class):
    client_socket = None

    def __init__(self, ip, port):
        super().__init__()
        self.setupUi(self)
        self.initialize_socket(ip, port)
        self.listen_thread()
        self.pushButton.clicked.connect(self.send_chat)

    def initialize_socket(self, ip, port):
        ''' tcp socket을 생성하고 server와 연결 '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))

    def send_chat(self):
        ''' message를 전송하는 버튼 콜백 함수 '''
        senders_name = self.lineEdit.text()
        data = self.sendmessage.text()
        message = (senders_name + ":" + data).encode('utf-8')
        self.receivemessage.addItem(message.decode('utf-8'))
        self.client_socket.send(message)
        self.sendmessage.clear()
        # self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def listen_thread(self):
        ''' 데이터 수신 Thread를 생성하고 시작한다 '''
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()

    def receive_message(self, so):
        while True:
            buf = so.recv(256)
            if not buf: # 연결이 종료됨
                break
            # self.chat_transcript_area.insert('end', buf.decode('utf-8') + '\n')
            # self.chat_transcript_area.yview(END)
            self.receivemessage.addItem(buf.decode('utf-8'))
        so.close()

if __name__ == "__main__":
    ip = input("server IP addr: ")
    if ip == '':
        ip = '10.10.21.119'
    port = 9051
    # ChatClient(ip, port)
    # mainloop()
    app = QApplication(sys.argv)
    mainWindow = Main(ip, port)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainWindow)
    widget.setFixedHeight(720)
    widget.setFixedWidth(650)
    widget.show()
    app.exec_()