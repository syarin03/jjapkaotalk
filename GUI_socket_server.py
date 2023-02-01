#섭씨온도를 보내고 화씨온도를 받아 표시하는 GUI 클라이언트 프로그램
import sys
from socket import *
import threading
import struct
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui
form_class = uic.loadUiType('./f.ui')[0]

class Main(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lineEdit.setText('')
        self.pushButton.clicked.connect(self.calculate)
    #섭씨 온도를 서버로 전송
    def calculate(self):
        global temp
        try :
            temp = float(self.lineEdit.text()) #섭씨 온도를 읽는다
        except:
            pass
        else:
            sock.send(str(temp).encode()) #섭씨 온도를 서버로 전송
    #Thread handler
    def handler(self,sock):
        while True:
            try : #수신 데이터가 없으면 예외 발생
                r_msg = sock.recv(1024) #메시지 수신
            except : #수신 데이터 없음
                pass
            else : #수신 데이터 표시
                self.lineEdit_2.clear()
                self.lineEdit_2.setText(str(r_msg.decode()))
                self.lineEdit.clear()

if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 2500))


    app = QApplication(sys.argv)
    mainWindow = Main()
    # 데이터 수신을 위한 스레드 생성과 실행
    cThread = threading.Thread(target=mainWindow.handler, args=(sock,))
    cThread.daemon = True
    cThread.start()
    mainWindow.setFixedHeight(600)
    mainWindow.setFixedWidth(600)
    mainWindow.show()
    app.exec_()