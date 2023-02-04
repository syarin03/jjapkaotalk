from main_client import *


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
        self.label_login_alert.setVisible(False)
        # endregion

        # region 페이지 이동
        self.btn_main_to_login.clicked.connect(self.go_login)
        self.btn_regist_result_to_login.clicked.connect(self.go_login)

        self.btn_main_to_regist.clicked.connect(self.go_regist)
        self.btn_login_to_regist.clicked.connect(self.go_regist)

        self.btn_main_to_chat.clicked.connect(self.go_chat)

        self.btn_login_to_find.clicked.connect(self.go_find)

        self.btn_login_to_main.clicked.connect(self.go_main)
        self.btn_regist_to_main.clicked.connect(self.go_main)
        self.btn_find_to_main.clicked.connect(self.go_main)
        self.btn_regist_result_to_main.clicked.connect(self.go_main)
        # endregion

        # self.btn_test.clicked.connect(self.test)
        self.btn_send_text.clicked.connect(self.send_text)
        self.btn_login.clicked.connect(self.login)
        self.btn_regist.clicked.connect(self.registration)

        self.input_chat_text.textChanged.connect(self.set_enabled_send)
        self.input_chat_text.returnPressed.connect(self.send_text)
        self.input_regist_id.editingFinished.connect(self.check_id)
        self.input_login_id.textChanged.connect(self.login_id_input_changed)
        self.input_regist_pw.textChanged.connect(self.pw_changed)
        self.input_regist_pwck.textChanged.connect(self.pw_changed)

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

    def login_id_input_changed(self):
        self.label_login_alert.setVisible(False)

    def send_text(self):
        # time = datetime.now().strftime('%F %T.%f')  # DB에 넣을 시간
        # msg_time = datetime.now().strftime('%H:%M')  # 출력할 시간
        chat = self.input_chat_text.text()
        self.thread.send_chat(1, chat)
        self.input_chat_text.clear()

    def append_message(self, dic_data):
        self.browser_chat.append(
            '<div style="text-align: right; vertical-align: bottom;">'
            '<span style="font-size: 10px; color: gray;">' + dic_data['send_time'] + '</span>'
            '<span style="font-size: 14px; color: black;"> ' + dic_data['message'] + '</span>'
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
        input_id = self.input_login_id.text()
        input_pw = self.input_login_pw.text()
        self.thread.send_login(input_id, input_pw)

    def logout(self):
        self.login_user = None
        QMessageBox.information(self, '알림', '로그아웃 되었습니다')

    def registration(self):
        if 0 in [len(self.input_regist_id.text()), len(self.input_regist_pw.text()), len(self.input_regist_pwck.text()),
                 len(self.input_regist_name.text()), len(self.input_regist_phone.text())]:
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
            self.thread.send_registration(regist_id, regist_pw, regist_name, regist_phone)

    def id_changed(self):
        self.isIDChecked = False
        self.btn_regist_idck.setEnabled(True)

    def pw_changed(self):
        if self.input_regist_pw.text().isdigit() or self.input_regist_pw.text().isalpha() or len(
                self.input_regist_pw.text()) < 8:
            self.label_regist_pw.setText('영문 숫자 혼용하여 8글자 이상이어야 합니다')
            self.isPWRuleChecked = False
        else:
            self.label_regist_pw.clear()
            self.isPWRuleChecked = True
        if self.input_regist_pw.text() != self.input_regist_pwck.text():
            self.label_regist_pwck.setText('비밀번호가 일치하지 않습니다')
            self.isPWSameChecked = False
        else:
            self.label_regist_pwck.clear()
            self.isPWSameChecked = True

    def check_id(self):
        print('check_id')
        self.thread.send_check_id(self.input_regist_id.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
