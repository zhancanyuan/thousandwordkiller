import traceback

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
import numpy as np
import matplotlib.pyplot as plt
import conn
import requests
import sys
import pandas as pd
import os
import urllib3.contrib.pyopenssl
from operateExcel import *
import requests
import bs4
import random
from playsound import playsound
from logistTest import *
import LoginAndRegist

urllib3.contrib.pyopenssl.inject_into_urllib3()


class TWKmain:

    def __init__(self):
        # 从文件中加载UI定义
        self.ui = uic.loadUi("ui/mainwindow.ui")
        # self.ui.setWindowFlags(Qt.FramelessWindowHint)
        # self.ui.setAttribute(Qt.WA_TranslucentBackground)
        self.locked = 1
        self.fromlogin = 0  # 判断是否从login界面登录进来 0否 1是
        self.uid = 1  # 登录用户id号
        self.data_in_recite = conn.mysqlsearch()  # 本地背单词已背数据
        self.res_in_recite = self.data_in_recite.get_default_user()  # 若不是从登录界面过来的，使用默认用户数据
        self.recite_word_row = int(self.res_in_recite[3])  # 初始化背单词的行数
        self.meaning_flag = 0  # 记录是否显示了中文意思 0无，1有
        self.test_first_click = 1  # 记录测试页面是否是第一次点击
        self.onlineTestType = 9  # 默认为任何单词
        self.onlineWordListIndex = 0  # 网上单词列表下标
        self.thelastword = 0  # 记录在线测试最后一个单词
        self.rIndex = 0  # 记录强化测试知道的单词列表下标
        self.right = []  # 强化测试中答对单词列表
        self.wrong = []  # 强化测试中答错单词列表
        self.hidden_click_times = 0  # 隐藏彩蛋按钮被点击次数
        self.index_of_tuici = 0  # 获取了推荐单词下标列表（self.tuici）的下标
        self.have_been_to_onlinerecite = 0  # 记录是否在在线背单词

        # 按键响应
        self.ui.userpagebtn.clicked.connect(self.gotouserpage)  # 个人中心按键被按下
        self.ui.searchwordbtn.clicked.connect(self.gotosearchpage)  # 在线搜索单词被按下
        self.ui.tologin.clicked.connect(self.gotologinpage)  # 退出按钮被按下
        self.ui.searchbtn.clicked.connect(self.youdaosearch)  # 在线搜索->搜索按键被按下
        self.ui.wordtestbtn.clicked.connect(self.gototestpage)  # 单词测试按键被按下
        self.ui.confirmbtn.clicked.connect(self.wordconfirm)  # 单词测试->确认提交答案按钮被按下
        self.ui.showresbtn.clicked.connect(self.showres)  # 单词测试->显示答案按钮被按下
        self.ui.playsoundbtn.clicked.connect(self.testplaysound)  # 单词测试->播放按钮
        self.ui.recitewordbtn.clicked.connect(self.gotorecitepage)  # 背单词按钮被按下
        self.ui.nextbtn.clicked.connect(self.nextword)  # 背单词->下一个按钮被按下
        self.ui.lastbtn.clicked.connect(self.lastword)  # 背单词->上一个按钮被按下
        self.ui.showmeaning.clicked.connect(self.wordmeaning)  # 背单词->显示中文按钮被按下
        self.ui.playsound.clicked.connect(self.play)  # 背单词->播放按钮被按下
        self.ui.localsearchbtn.clicked.connect(self.gotolocalsearch)  # 跳转到本地查词
        self.ui.localsearchpagebtn.clicked.connect(self.search)  # 本地查询->查询键按下
        self.ui.returntouserpage.clicked.connect(self.gotouserpage)  # 联系界面转用户界面
        self.ui.ourcontact.clicked.connect(self.gotocontact)  # 转到联系界面
        self.ui.wronglist.clicked.connect(self.gotowronglist)  # 转到错题集
        self.ui.onlineTestbtn.clicked.connect(self.gotoOnlineTest)  # 跳转到在线测试
        self.ui.IELTSbtn.clicked.connect(self.setNine)  # 在线测试第九个选项，雅思
        self.ui.toeflbtn.clicked.connect(self.setSeven)  # 在线测试第七的选项，托福
        self.ui.GMATbtn.clicked.connect(self.setOne)  # 在线测试第一个选项，GMAT
        self.ui.kaoyanbtn.clicked.connect(self.setTwo)  # 在线测试第二个选项，考研
        self.ui.cet6btn.clicked.connect(self.setFive)  # 在线测试第五个选项，六级
        self.ui.cet4btn.clicked.connect(self.setFour)  # 在线测试第四个选项，四级
        self.ui.gaokaobtn.clicked.connect(self.setThree)  # 在线测试第三个选项，高考
        self.ui.engprobtn.clicked.connect(self.setSix)  # 在线测试第六个选项，英专
        self.ui.GREbtn.clicked.connect(self.setEight)  # 在线测试第八个选项，GRE
        self.ui.anybtn.clicked.connect(self.setTen)  # 在线测试第十个选项，以上九个中任意单词
        self.ui.know.clicked.connect(self.knowit)  # 在线测试->知道按钮
        self.ui.dontknow.clicked.connect(self.dontknowit)  # 在线测试->不知道按钮
        self.ui.showtrans.clicked.connect(self.showtranslation)  # 在线测试->显示释义按钮
        self.ui.reinforcebtn.clicked.connect(self.gotoReinforceTest)  # 在线测试之后，进入强化测试（基于在线测试知道的单词列表进行中文4选1）
        self.ui.checkandnext.clicked.connect(self.judge)  # 强化测试确定按钮
        self.ui.gobacktestmain.clicked.connect(self.gotoOnlineTest)  # 强化测试之后，有单词没掌握页面‘回到测试页面’按钮
        self.ui.gobacktestmain2.clicked.connect(self.gotoOnlineTest)  # 强化测试之后，全部单词都掌握‘会到测试页面’按钮
        self.ui.hidden.clicked.connect(self.surprise)  # 隐藏按键，点击6下出现飞机大战按钮
        self.ui.spacewar.setVisible(False)  # 隐藏彩蛋按键
        self.ui.spacewar.clicked.connect(self.airplane)  # 飞机大战按键
        self.ui.online_recite_btn.clicked.connect(self.gotoOnlineRecite)  # 在线背单词跳转
        self.ui.testline.clicked.connect(self.showline)  # 个人中心测试曲线按钮
        self.ui.reci_next_word_btn.clicked.connect(self.OnlineReciteNext)  # 在线背单词下一个词按钮
        self.ui.reci_last_word_btn.clicked.connect(self.OnlineReciteLast)  # 在线背单词上一个词按钮
        self.ui.reci_show_mean_btn.clicked.connect(self.OnlineReciteShowTranslation)  # 在线背单词显示释义按钮
        self.ui.returnuser.clicked.connect(self.returntouserpage)  # 在线背单词完成后，返回用户中心按钮

        # 读取图片图标，因为qt样式不能直接获取相对路径，所以在python中获取路径后再set样式
        url_father = os.path.dirname(os.path.abspath(__file__))
        url = ""
        for i in url_father:
            if i == "\\":
                url = url + "/"
            else:
                url = url + i
        self.ui.frame_2.setStyleSheet("border-image:url(" + url + "/ui/user_photo.jpg)")  # 默认用户头像图片
        self.ui.setWindowIcon(QIcon(url+"/ui/icon.ico"))  # 程序图标

    # 在线背单词完成后返回用户中心方法
    def returntouserpage(self):
        self.have_been_to_onlinerecite == 0
        self.index_of_tuici = 0
        self.ui.stackedWidget.setCurrentIndex(1)

    # 在线背单词(根据错题集rank，pk推词)
    def gotoOnlineRecite(self):
        self.ui.stackedWidget.setCurrentIndex(14)
        if self.have_been_to_onlinerecite == 0:
            self.have_been_to_onlinerecite = 1
            # 扇贝网爬虫，获取英语单词
            category_res = requests.get('https://www.shanbay.com/api/v1/vocabtest/category/?_=1566889802182', verify=False)
            category_json = category_res.json()
            category_data = category_json['data']

            url = 'https://www.shanbay.com/api/v1/vocabtest/vocabularies/'
            headers = {
                'Referer': 'https://www.shanbay.com/vocabtest/',
                'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 83.0.4103.116Safari / 537.36'
            }
            params = {
                'category': category_data[9][0],
                '_': '1566889452889'
            }  # 默认出题范围为全部
            res = requests.get(url, headers=headers, params=params, verify=False)
            jsonres = res.json()

            self.online_vacabularies = jsonres['data']

            new_ranks = []
            new_pk = []

            new_words = []

            for va in self.online_vacabularies:
                new_words.append([va['rank'], va['pk']])

            # print(new_words)
            new_w = np.array(new_words)

            try:
                # 若不是从用户登录窗口进来的，默认使用数据库中第一个用户的数据，若是从登录界面进来的，读取对应用户的错词本
                if self.fromlogin == 0:
                    path = f'{os.getcwd()}\的错词本.xls'
                else:
                    un = self.ui.username.text()
                    un += '的错词本.xls'
                    path = f'{os.getcwd()}'
                    path += '\\'
                    path += un
                self.onlinePath = path
                self.tuici = LogistPredict(path, new_w)
                print(self.tuici)
                self.length_of_tuici = len(self.tuici)
                self.ui.reci_show_box.setText("")
                # self.ol_reci_df = pd.read_excel(self.onlinePath)
                print("df ok!")
                self.OnlineReciteShowWord()
                # 如果推词列表为空，说明词库还不够多，跳转到提醒界面并重置下标和标志位
                if self.length_of_tuici == 0:
                    self.ui.stackedWidget.setCurrentIndex(16)
                    self.index_of_tuici = 0
                    self.have_been_to_onlinerecite = 0
            except:
                # 因为词库单词不够多会引发错误并退出，所以traceback之后再跳转到提醒界面
                traceback.print_exc()
                self.ui.stackedWidget.setCurrentIndex(16)
                self.index_of_tuici = 0
                self.have_been_to_onlinerecite = 0

    # 在线背单词显示单词方法
    def OnlineReciteShowWord(self):
        try:
            if 0 <= self.index_of_tuici < self.length_of_tuici:
                self.online_vacabulary = self.online_vacabularies[self.tuici[self.index_of_tuici]]
                # print(self.online_vacabulary)
                self.online_vacabu = self.online_vacabulary['content']
                s = "%d/%d" % (self.index_of_tuici + 1, self.length_of_tuici)
                self.ui.reci_show_box.setText(s)
                self.ui.reci_show_box.append('')
                self.ui.reci_show_box.append(self.online_vacabu)
        except:
            traceback.print_exc()

    # 在线背单词显示释义方法
    def OnlineReciteShowTranslation(self):
        # 防止数组越界
        if 0 <= self.index_of_tuici < self.length_of_tuici:
            try:
                for d in self.online_vacabularies[self.tuici[self.index_of_tuici]]["definition_choices"]:
                    if d['rank'] == self.online_vacabularies[self.tuici[self.index_of_tuici]]['rank']:
                        self.online_translation = d['definition']
                        print(self.online_translation)
                self.ui.reci_show_box.append(self.online_translation)
            except:
                traceback.print_exc()

    # 在线背单词下一个单词方法
    def OnlineReciteNext(self):
        if self.index_of_tuici < self.length_of_tuici - 1:
            self.index_of_tuici += 1
            self.OnlineReciteShowWord()
        # 若是最后一个单词要注意，背完之后点击下一个要跳转到完成界面，防止数组越界
        elif self.index_of_tuici == self.length_of_tuici - 1:
            self.ui.stackedWidget.setCurrentIndex(15)
            self.index_of_tuici = 0
            self.have_been_to_onlinerecite = 0

    # 在线背单词上一个单词方法
    def OnlineReciteLast(self):
        if self.index_of_tuici > 0:
            self.index_of_tuici -= 1
            self.OnlineReciteShowWord()

    # 展示错题集曲线
    def showline(self):
        # 数据是否要标准化
        try:
            scale = False
            if self.fromlogin == 0:
                path = f'{os.getcwd()}\的错词本.xls'
            else:
                un = self.ui.username.text()
                un += '的错词本.xls'
                path = f'{os.getcwd()}'
                path += '\\'
                path += un
            df = pd.read_excel(path)
            # 今日份需背单词
            rp = df[['rank', 'pk']]
            b = df[['是否记得']]
            x_data = np.array(rp)
            y_data = np.array(b)
            y_data2 = np.array(df['是否记得'])
            x0 = []
            y0 = []
            x1 = []
            y1 = []
            for i in range(len(x_data)):
                if int(y_data[i]) == 0:
                    x0.append(int(x_data[i, 0]))
                    y0.append(int(x_data[i, 1]))
                else:
                    x1.append(int(x_data[i, 0]))
                    y1.append(int(x_data[i, 1]))
            # plt.scatter(x_data,y_data)
            plt.plot(x0, y0, 'r.', marker='x')
            plt.plot(x1, y1, 'b.', marker='o')

            plt.legend(labels={'remember', 'forget'}, loc='best')
            plt.show()
        except:
            traceback.print_exc()

    # 显示飞机大战按钮
    def surprise(self):
        if self.hidden_click_times >= 5:
            self.ui.spacewar.setVisible(True)
        self.hidden_click_times += 1

    # 开始飞机大战
    def airplane(self):
        try:
            import spacewarmain
            spacewarmain.main()
            self.ui.spacewar.setVisible(False)
            self.hidden_click_times = 0
        except:
            traceback.print_exc()

    # 转到个人中心
    def gotouserpage(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        if self.fromlogin == 0:
            self.data = conn.mysqlsearch()
            self.res = self.data.get_default_user()
            # print(self.res)
            self.default_username = str(self.res[1])
            self.default_user_killed = str(self.res[3])
            self.ui.username.setText(self.default_username)
            self.ui.wordcount.setText(self.default_user_killed)
        elif self.fromlogin == 1:
            self.data = conn.mysqlsearch()
            self.res = self.data.get_userinfo()
            # print(self.res)
            self.current_username = str(self.res[self.uid - 1]['usrname'])
            self.current_user_killed = str(self.res[self.uid - 1]['killedwords'])
            self.ui.username.setText(self.current_username)
            self.ui.wordcount.setText(self.current_user_killed)

    # 转到在线查词页面
    def gotosearchpage(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    # 退出登录
    def gotologinpage(self):
        try:
            self.ui.close()
            self.loginwindow = LoginAndRegist.LoginWindow()
            self.loginwindow.ui.show()
        except:
            traceback.print_exc()

    # 在线搜索函数
    def youdaosearch(self):
        content = self.ui.searchbox.text()
        if content == '':
            self.ui.textBrowser.setText("请输入待查询的单词！")
            return
        try:
            url = 'http://www.youdao.com/w/' + content + '/'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
            }
            res = requests.get(url, headers=headers)
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            targets = soup.find("div", class_="trans-container")
            print(targets.ul.text)
            self.ui.textBrowser.setText(targets.ul.text)

        except:
            self.ui.textBrowser.setText("没有查到这个单词，请重新输入")  # 可能返回的数据有误或有道查不到这个单词

    # 本地搜索函数
    def search(self):
        print("search!")
        try:
            path = f'{os.getcwd()}\Speech_US\TestingWords.xls'
            # print("Wordlist load!")
            df = pd.read_excel(path)
            # print("df ok!")

            # 词汇表
            rows = df.loc[:, ].values[0:len(df) + 1]
            # print("searching...")
            self.searching(len(df), self.ui.localsearchbox.text(), rows)
        except ImportError as ie:
            print("ImportError: %s" % ie)

    # 被调用的本地搜索函数
    def searching(self, ran, Word, rows):
        self.ui.localsearchshow.setText("本地词库没有这个单词！")
        for i in range(ran):
            if Word == rows[i][0]:
                print(rows[i][1])
                self.ui.localsearchshow.setText(rows[i][1])
            elif Word in rows[i][1] and self.isChinese(Word):
                print(rows[i][0])
                if self.ui.localsearchshow.toPlainText() == "本地词库没有这个单词！":
                    self.ui.localsearchshow.setText(rows[i][0])
                    self.ui.localsearchshow.append(rows[i][1])
                    self.ui.localsearchshow.append('')
                    continue
                self.ui.localsearchshow.append(rows[i][0])
                self.ui.localsearchshow.append(rows[i][1])
                self.ui.localsearchshow.append("")
        # else:
        #     self.ui.localsearchshow.setText("本地词库没有这个单词")

    # 判断是否为中文
    def isChinese(self, s):
        for each in s:
            if u'\u4e00' <= each <= u'\u9fff':
                return True
            return False

    # 单词测试（本地）界面及其按钮响应
    def gototestpage(self):
        if self.test_first_click == 1:
            self.test_first_click = 0
            self.ui.resultshow.setText("")
            self.ui.answer.setText("")
            self.path = f'{os.getcwd()}\Speech_US\TestingWords.xls'
            print("Wordlist load!")
            self.df = pd.read_excel(self.path)
            print("df ok!")
            # 词汇表
            self.rows = self.df.loc[:, ].values[0:len(self.df) + 1]
            self.num = random.randint(0, len(self.df) + 1)
            self.ui.wordshow.setText(self.rows[self.num][1])
        self.ui.stackedWidget.setCurrentIndex(2)

    # 本地单词测试播放音频
    def testplaysound(self):
        try:
            self.soundpath_in_test = f'{os.getcwd()}\Speech_US'
            print("soundpath in test ok")
            self.soundpath2_in_test = r'\\' + self.rows[self.num][0] + r'.mp3'
            print("soundpath2 in test ok")
            self.soundpath_in_test += self.soundpath2_in_test
            print(self.soundpath_in_test)
            playsound(self.soundpath_in_test)
        except:
            print("cannot find sound file")

    # 本地单词测试确认事件
    def wordconfirm(self):
        ans = self.ui.answer.text()
        try:
            if ans != self.rows[self.num][0]:
                print("ans wrong!")
                self.ui.resultshow.setText("ans wrong!")
            else:
                self.ui.resultshow.setText("")
                self.ui.answer.setText("")
                self.num = random.randint(0, len(self.df) + 1)
                self.ui.wordshow.setText(self.rows[self.num][1])
        except:
            self.ui.resultshow.setText("出错了")

    # 本地单词测试显示答案
    def showres(self):
        self.ui.resultshow.setText(self.rows[self.num][0])

    # 本地背单词页面及其按钮响应
    def gotorecitepage(self):
        if self.fromlogin == 1 and self.locked == 1:
            self.recite_word_row = int(self.ui.wordcount.text())
            self.locked = 0
        pshow = "%d/3070" % self.recite_word_row
        self.ui.progressshow.setText(pshow)
        if self.meaning_flag == 1:
            self.ui.stackedWidget.setCurrentIndex(3)
            return
        self.ui.stackedWidget.setCurrentIndex(3)
        self.recitepath = f'{os.getcwd()}\Speech_US\TestingWords.xls'
        self.recite_df = pd.read_excel(self.recitepath)
        # 词汇表
        self.reciterows = self.recite_df.loc[:, ].values[0:len(self.recite_df) + 1]
        self.ui.reciteshow.setText(self.reciterows[self.recite_word_row][0])

    # 本地背单词下一个单词
    def nextword(self):
        if self.recite_word_row < 3070:
            pshow = "%d/3070" % self.recite_word_row
            self.ui.progressshow.setText(pshow)
            self.meaning_flag = 0
            self.recite_word_row += 1
            self.updatekilledword = conn.mysqlsearch()
            sql = "UPDATE usr SET killedwords = %s WHERE ID = %s" % (str(self.recite_word_row), str(self.uid))
            cursor = self.updatekilledword.conn.cursor()
            try:
                cursor.execute(sql)
                self.updatekilledword.conn.commit()
            except:
                print("update error!")
                self.updatekilledword.conn.rollback()
            self.gotorecitepage()

    # 本地背单词上一个单词
    def lastword(self):
        if self.recite_word_row >= 1:
            pshow = "%d/3070" % self.recite_word_row
            self.ui.progressshow.setText(pshow)
            self.meaning_flag = 0
            self.recite_word_row -= 1
            self.gotorecitepage()

    # 本地背单词显示释义按钮响应事件
    def wordmeaning(self):
        if self.meaning_flag == 0:
            self.ui.reciteshow.append(self.reciterows[self.recite_word_row][1])
            self.meaning_flag = 1

    # 本地背单词播放声音按钮响应事件
    def play(self):
        self.soundpath = f'{os.getcwd()}\Speech_US'
        # print("soundpath ok")
        self.soundpath2 = r'\\' + self.reciterows[self.recite_word_row][0] + r'.mp3'
        # print("soundpath2 ok")
        self.soundpath += self.soundpath2
        playsound(self.soundpath)

    # 跳转到本地搜词页面
    def gotolocalsearch(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    # 跳转到联系我们页面
    def gotocontact(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    # 跳转到错题集页面
    def gotowronglist(self):
        if self.fromlogin == 0:
            self.ui.stackedWidget.setCurrentIndex(6)
            path = f'{os.getcwd()}\的错词本.xls'
            # print("Wordlist load!")
            df = pd.read_excel(path)
            # print("df ok!")
        elif self.fromlogin == 1:
            un = self.ui.username.text()
            un += '的错词本.xls'
            path = f'{os.getcwd()}'
            path += '\\'
            path += un
            print(path)
            df = pd.read_excel(path)
            self.ui.stackedWidget.setCurrentIndex(6)

        # 词汇表
        rows = df.loc[:, ].values[0:len(df) + 1]

        self.ui.wrongwordlist.setText('')

        for i in range(1, len(df)):
            if rows[i][5] == 1 or rows[i][4] == 0:
                self.ui.wrongwordlist.append(rows[i][0])
                self.ui.wrongwordlist.append(rows[i][1])
                self.ui.wrongwordlist.append('')

    # 在线测试页面每个按钮响应函数
    def setOne(self):
        self.onlineTestType = 1
        self.onlineWordListIndex = 0
        self.thelastword = 0
        self.onlinetest_init()
        self.onlineTestStart()

    def setTwo(self):
        self.onlineTestType = 2
        self.onlineWordListIndex = 0
        self.thelastword = 0
        self.onlinetest_init()
        self.onlineTestStart()

    def setThree(self):
        self.onlineTestType = 3
        self.onlineWordListIndex = 0
        self.thelastword = 0
        self.onlinetest_init()
        self.onlineTestStart()

    def setFour(self):
        self.onlineTestType = 4
        self.onlineWordListIndex = 0
        self.thelastword = 0
        self.onlinetest_init()
        self.onlineTestStart()

    def setFive(self):
        self.onlineTestType = 5
        self.onlineWordListIndex = 0
        self.thelastword = 0
        self.onlinetest_init()
        self.onlineTestStart()

    def setSix(self):
        self.onlineTestType = 6
        self.onlineWordListIndex = 0
        self.thelastword = 0
        self.onlinetest_init()
        self.onlineTestStart()

    def setSeven(self):
        self.onlineTestType = 7
        self.onlineWordListIndex = 0
        self.thelastword = 0
        self.onlinetest_init()
        self.onlineTestStart()

    def setEight(self):
        self.onlineTestType = 8
        self.onlineWordListIndex = 0
        self.thelastword = 0
        self.onlinetest_init()
        self.onlineTestStart()

    def setNine(self):
        self.onlineTestType = 9
        self.onlineWordListIndex = 0
        self.thelastword = 0
        self.onlinetest_init()
        self.onlineTestStart()

    def setTen(self):
        self.onlineTestType = 10
        self.onlineWordListIndex = 0
        self.thelastword = 0
        self.onlinetest_init()
        self.onlineTestStart()

    # 跳转到在线测试界面
    def gotoOnlineTest(self):
        self.ui.stackedWidget.setCurrentIndex(7)

    # 在线测试初始化
    def onlinetest_init(self):
        category_res = requests.get('https://www.shanbay.com/api/v1/vocabtest/category/?_=1566889802182', verify=False)
        category_json = category_res.json()
        category_data = category_json['data']
        url = 'https://www.shanbay.com/api/v1/vocabtest/vocabularies/'
        headers = {
            'Referer': 'https://www.shanbay.com/vocabtest/',
            'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 83.0.4103.116Safari / 537.36'
        }
        params = {
            'category': category_data[self.onlineTestType - 1][0],
            '_': '1566889452889'
        }

        res = requests.get(url, headers=headers, params=params, verify=False)
        jsonres = res.json()

        self.vacabularies = jsonres['data']
        print(self.vacabularies)
        self.knows = []
        self.unknows = []

    # 在线测试开始
    def onlineTestStart(self):
        self.ui.stackedWidget.setCurrentIndex(8)
        # print("start!")
        self.vacabulary = self.vacabularies[self.onlineWordListIndex]
        self.vacabu = self.vacabulary['content']
        print(self.vacabu)
        num = self.onlineWordListIndex + 1
        print(num)
        # print('第' + num + '个：' + vacabu)
        prog = '%d/50\n\n' % num
        s = '%s' % self.vacabu
        s = prog + s
        self.ui.onlinetestshow.setText(s)

    # 测试界面，下一个词（包含在知道和不知道）
    def online_nextword(self):
        try:
            self.onlineWordListIndex += 1
            self.onlineTestStart()
        except IndexError as ie:
            print("IndexError:%s" % ie)

    # 知道按钮
    def knowit(self):
        self.gettranslation()
        value = [self.vacabu, self.translation, f'{self.vacabulary["rank"]}', f'{self.vacabulary["pk"]}', '1', '0']
        print(value)
        if self.onlineWordListIndex < 49:
            # print("in if")
            if self.fromlogin == 0:
                update_note_xls('的错词本.xls', value, 1)
                # print("update ok")
                self.knows.append(self.onlineWordListIndex)
                self.online_nextword()
            elif self.fromlogin == 1:
                un = self.ui.username.text()
                un += '的错词本.xls'
                update_note_xls(un, value, 1)
                # print("update ok")
                self.knows.append(self.onlineWordListIndex)
                self.online_nextword()

        elif self.onlineWordListIndex == 49 and self.thelastword == 0:
            self.thelastword = 1
            # print("in if")
            if self.fromlogin == 0:
                update_note_xls('的错词本.xls', value, 1)
                # print("update ok")
                self.knows.append(self.onlineWordListIndex)
            elif self.fromlogin == 1:
                un = self.ui.username.text()
                un += '的错词本.xls'
                update_note_xls(un, value, 1)
                # print("update ok")
                self.knows.append(self.onlineWordListIndex)

            self.ui.stackedWidget.setCurrentIndex(9)
            self.wordsknow = len(self.knows)
            self.wordsdontknow = len(self.unknows)
            s = "以下为测试结果：\n\n认识%d个单词，不认识%d个单词" % (self.wordsknow, self.wordsdontknow)
            self.ui.onlineTestResShow.setText(s)
            if len(self.knows) == 0:
                self.ui.stackedWidget.setCurrentIndex(13)

    # 不知道按钮
    def dontknowit(self):
        self.gettranslation()
        if self.onlineWordListIndex < 49:
            if self.fromlogin == 0:
                update_note_xls('的错词本.xls',
                                [self.vacabu, self.translation, f'{self.vacabulary["rank"]}',
                                 f'{self.vacabulary["pk"]}',
                                 '0', '1'], 0)
                print("update ok!")
                self.unknows.append(self.onlineWordListIndex)
                self.online_nextword()
            elif self.fromlogin == 1:
                un = self.ui.username.text()
                un += '的错词本.xls'
                update_note_xls(un,
                                [self.vacabu, self.translation, f'{self.vacabulary["rank"]}',
                                 f'{self.vacabulary["pk"]}',
                                 '0', '0'], 0)
                self.unknows.append(self.onlineWordListIndex)
                self.online_nextword()
        elif self.onlineWordListIndex == 49 and self.thelastword == 0:
            self.thelastword = 1
            if self.fromlogin == 0:
                update_note_xls('的错词本.xls',
                                [self.vacabu, self.translation, f'{self.vacabulary["rank"]}',
                                 f'{self.vacabulary["pk"]}',
                                 '0', '0'], 0)
            elif self.fromlogin == 1:
                un = self.ui.username.text()
                un += '的错词本.xls'
                update_note_xls(un,
                                [self.vacabu, self.translation, f'{self.vacabulary["rank"]}',
                                 f'{self.vacabulary["pk"]}',
                                 '0', '0'], 0)

            self.unknows.append(self.onlineWordListIndex)
            self.ui.stackedWidget.setCurrentIndex(9)
            self.wordsknow = len(self.knows)
            print(self.wordsknow)
            self.wordsdontknow = len(self.unknows)
            print(self.wordsdontknow)
            s = "以下为测试结果：\n\n认识%d个单词，不认识%d个单词" % (self.wordsknow, self.wordsdontknow)
            print(s)
            self.ui.onlineTestResShow.setText(s)
            if len(self.knows) == 0:
                self.ui.stackedWidget.setCurrentIndex(13)

    # 获取单词释义
    def gettranslation(self):
        for d in self.vacabularies[self.onlineWordListIndex]["definition_choices"]:
            if d['rank'] == self.vacabularies[self.onlineWordListIndex]['rank']:
                self.translation = d['definition']

    # 显示释义按钮
    def showtranslation(self):
        self.gettranslation()
        self.ui.onlinetestshow.append('')
        self.ui.onlinetestshow.append(self.translation)

    # 跳转到强化测试页面
    def gotoReinforceTest(self):
        self.ui.stackedWidget.setCurrentIndex(10)
        print("in reinforce")
        self.know = self.knows[self.rIndex]
        print("know ok")
        self.vacabulary_know = self.vacabularies[self.know]
        print("vk ok")
        self.wordInReinforce = self.vacabulary_know['content']
        print()
        print(self.wordInReinforce)

        self.ui.Achoose.setChecked(False)
        self.ui.Bchoose.setChecked(False)
        self.ui.Cchoose.setChecked(False)
        self.ui.Dchoose.setChecked(False)

        self.definitions = self.vacabulary_know['definition_choices']
        self.ui.reinforceshow.setText(self.wordInReinforce)
        self.ui.Alabel.setText(self.definitions[0]['definition'])
        self.ui.Blabel.setText(self.definitions[1]['definition'])
        self.ui.Clabel.setText(self.definitions[2]['definition'])
        self.ui.Dlabel.setText(self.definitions[3]['definition'])

    # 判断选择哪一个答案
    def judge(self):
        self.lengthofknows = len(self.knows)
        if self.ui.Achoose.isChecked():
            if self.rIndex < self.lengthofknows - 1:
                rank = self.definitions[0]['rank']
                if rank == self.vacabulary_know['rank']:
                    self.right.append(self.wordInReinforce)
                else:
                    self.wrong.append(self.wordInReinforce)
                print(self.right)
                print(self.wrong)
                self.rIndex += 1
                self.gotoReinforceTest()
            elif self.rIndex == self.lengthofknows - 1:
                if len(self.wrong) == 0:
                    self.ui.stackedWidget.setCurrentIndex(12)
                else:
                    self.ui.stackedWidget.setCurrentIndex(11)
                    wlist = '\n'.join(self.wrong)
                    self.ui.textBrowser_2.setText(wlist)
        elif self.ui.Bchoose.isChecked():
            if self.ui.Bchoose.isChecked():
                if self.rIndex < self.lengthofknows - 1:
                    rank = self.definitions[1]['rank']
                    if rank == self.vacabulary_know['rank']:
                        self.right.append(self.wordInReinforce)
                    else:
                        self.wrong.append(self.wordInReinforce)
                    print(self.right)
                    print(self.wrong)
                    self.rIndex += 1
                    self.gotoReinforceTest()
                elif self.rIndex == self.lengthofknows - 1:
                    if len(self.wrong) == 0:
                        self.ui.stackedWidget.setCurrentIndex(12)
                    else:
                        self.ui.stackedWidget.setCurrentIndex(11)
                        wlist = '\n'.join(self.wrong)
                        self.ui.textBrowser_2.setText(wlist)
        elif self.ui.Cchoose.isChecked():
            if self.ui.Cchoose.isChecked():
                if self.rIndex < self.lengthofknows - 1:
                    rank = self.definitions[2]['rank']
                    if rank == self.vacabulary_know['rank']:
                        self.right.append(self.wordInReinforce)
                    else:
                        self.wrong.append(self.wordInReinforce)
                    print(self.right)
                    print(self.wrong)
                    self.rIndex += 1
                    self.gotoReinforceTest()
                elif self.rIndex == self.lengthofknows - 1:
                    if len(self.wrong) == 0:
                        self.ui.stackedWidget.setCurrentIndex(12)
                    else:
                        self.ui.stackedWidget.setCurrentIndex(11)
                        wlist = '\n'.join(self.wrong)
                        self.ui.textBrowser_2.setText(wlist)
        elif self.ui.Dchoose.isChecked():
            if self.ui.Dchoose.isChecked():
                if self.rIndex < self.lengthofknows - 1:
                    rank = self.definitions[3]['rank']
                    if rank == self.vacabulary_know['rank']:
                        self.right.append(self.wordInReinforce)
                    else:
                        self.wrong.append(self.wordInReinforce)
                    print(self.right)
                    print(self.wrong)
                    self.rIndex += 1
                    self.gotoReinforceTest()
                elif self.rIndex == self.lengthofknows - 1:
                    if len(self.wrong) == 0:
                        self.ui.stackedWidget.setCurrentIndex(12)
                    else:
                        self.ui.stackedWidget.setCurrentIndex(11)
                        wlist = '\n'.join(self.wrong)
                        self.ui.textBrowser_2.setText(wlist)

        elif not self.ui.Achoose.isChecked() and not self.ui.Bchoose.isChecked() and not self.ui.Cchoose.isChecked() \
                and not self.ui.Dchoose.isChecked():
            QMessageBox.warning(self.ui,
                                "警告",
                                "请选择一个答案",
                                QMessageBox.Yes)


if __name__ == "__main__":
    app = QApplication([])
    w = TWKmain()
    w.fromlogin = 0
    w.ui.show()
    app.exec_()
