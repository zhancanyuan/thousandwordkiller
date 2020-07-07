import traceback

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox
import twkmain
import conn
import os
from operateExcel import *


class LoginWindow:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = uic.loadUi("ui/login.ui")
        self.ui.loginbtn.clicked.connect(self.login)
        self.ui.registbtn.clicked.connect(self.goregist)

        # 读取图片图标，因为qt样式不能直接获取相对路径，所以在python中获取路径后再set样式
        url_father = os.path.dirname(os.path.abspath(__file__))
        url = ""
        for i in url_father:
            if i == "\\":
                url = url + "/"
            else:
                url = url + i
        self.ui.frame.setStyleSheet("border-image:url(" + url + "/ui/1.jpg)")
        self.ui.setWindowIcon(QIcon(url + "/ui/icon.ico"))

    def login(self):
        try:
            obj = conn.mysqlsearch()
            result = obj.get_userinfo()
            ulist = []  # 用户名列表
            plist = []  # 密码列表
            kwlist = []  # 已背单词列表
            idlist = []  # id list
            login_user = self.ui.usernamebox.text()
            login_password = self.ui.pwdbox.text()
            print(login_user, login_password)

            for item in result:
                ulist.append(item['usrname'])
                plist.append(str(item['password']))
                kwlist.append(item['killedwords'])
                idlist.append(item['id'])
            deter = True
        except:
            traceback.print_exc()

        for i in range(len(ulist)):
            while True:
                try:
                    if login_user == ulist[i] and login_password == plist[i]:
                        self.ui.close()
                        self.twkmainw = twkmain.TWKmain()
                        self.twkmainw.fromlogin = 1
                        self.twkmainw.uid = idlist[i]
                        self.twkmainw.ui.show()
                        # print("show ok")
                        killedwordsnum = kwlist[i]
                        # print("num ok")
                        self.twkmainw.ui.username.setText(login_user)
                        # print("user ok")
                        self.twkmainw.ui.wordcount.setText(str(killedwordsnum))
                        print("登录成功！用户名：%s 密码： %s" % (login_user, login_password))
                        deter = False
                        break
                    else:
                        break
                except:
                    traceback.print_exc()
        while deter:
            QMessageBox.warning(self.ui,
                                "警告",
                                "用户名或密码错误！",
                                QMessageBox.Yes)
            self.ui.usernamebox.setFocus()
            break

    def goregist(self):
        self.ui.close()
        self.regwin = RegistWindow()
        self.regwin.ui.show()


class RegistWindow:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = uic.loadUi("ui/regist.ui")
        self.ui.gobackbtn.clicked.connect(self.goback)
        self.ui.regbtn.clicked.connect(self.regist)

        # 读取图片图标，因为qt样式不能直接获取相对路径，所以在python中获取路径后再set样式
        url_father = os.path.dirname(os.path.abspath(__file__))
        url = ""
        for i in url_father:
            if i == "\\":
                url = url + "/"
            else:
                url = url + i
        self.ui.frame.setStyleSheet("border-image:url(" + url + "/ui/1.jpg)")
        self.ui.setWindowIcon(QIcon(url + "/ui/icon.ico"))

    def goback(self):
        self.ui.close()
        self.lgwin = LoginWindow()
        self.lgwin.ui.show()

    def regist(self):
        regist_user = self.ui.usernamebox.text()
        regist_password = self.ui.pwdbox.text()
        regist_passwprd_confirm = self.ui.pwdconbox.text()
        print(regist_user, regist_passwprd_confirm)

        if regist_password != regist_passwprd_confirm:
            QMessageBox.warning(self.ui,
                                "警告",
                                "两次输入的密码不一致！",
                                QMessageBox.Yes)
            return
        obj_r = conn.mysqlsearch()
        res = obj_r.insert_userinfo(regist_user, regist_password)  # 接收返回参数，3为注册成功，1，2，4不成功
        if res == 3:
            QMessageBox.information(self.ui, "成功！", "注册成功！")
            self.ui.usernamebox.setFocus()
            # 创建错词本
            my_book_name_xls = '%s的错词本.xls' % regist_user
            my_sheet_name_xls = '在线背诵错词表'
            my_value_title = [["单词", "中文", "rank", "pk", "是否记得", "错误次数"], ]

            my_value2 = []
            my_value1 = []

            write_excel_xls(my_book_name_xls, my_sheet_name_xls, my_value_title)
            append_note_xls(my_book_name_xls, my_value1, 1)
            append_note_xls(my_book_name_xls, my_value2, 1)
            read_note_xls(my_book_name_xls)

        elif res == 1:
            QMessageBox.warning(self.ui,
                                "警告",
                                "用户名或密码为空！",
                                QMessageBox.Yes)
        elif res == 2:
            QMessageBox.warning(self.ui,
                                "警告",
                                "用户名已存在！",
                                QMessageBox.Yes)
        elif res == 4:
            QMessageBox.warning(self.ui,
                                "警告",
                                "出现错误！",
                                QMessageBox.Yes)


if __name__ == "__main__":
    app = QApplication([])
    w = LoginWindow()
    w.ui.show()
    app.exec_()
