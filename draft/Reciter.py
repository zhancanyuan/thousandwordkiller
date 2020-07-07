#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple

import numpy as np
import pandas as pd
import xlrd
import os

from playsound import playsound

# import sys
# from PyQt5 import QtWidgets

if __name__=="__main__":
    path = f'{os.getcwd()}\Speech_US\TestingWords.xls'
    print('Welcome to 摞你命单词 自测, enjoy')


    ranMin = int(input('请输入范围最小值'))
    ranMax=int(input('请输入范围最大值'))
    df=pd.read_excel(path)

    #今日份需背单词
    rows=df.loc[:,].values[ranMin-2:ranMax-1]

    while 1:
        choice=input('Test or recite? [T/R]')
        if choice=='exit':
            break
        if choice=='T':
            print('Test')
            #numpy乱序
            rows=np.random.permutation(rows)

            mistakes=0
            ran=ranMax-ranMin+1

            for i in range(ran):
                print(f'{rows[i][0]} ')

                #音频
                soundpath=f'{os.getcwd()}\Speech_US'
                soundpath2=r'\\'+rows[i][0]+r'.mp3'
                soundpath+=soundpath2

                playsound(soundpath)

                recation=input('')
                if recation=='\v':
                    print(rows[i][1])
                else:
                    print(rows[i][1])

                print('-'*35)
            #测试
            #     anwser=input('>>')
            #     if anwser==rows[i][0]:
            #         print('正确')
            #         print('')
            #     else:
            #         print(f'答案错误！ 正确答案是:{rows[i][0]}')
            #         print('')
            #         mistakes+=1
            #
            # print(f'练习结束，错题数为{mistakes},正确率为{int((ran-mistakes)/(ran)*100)}%')

        else:
            ran = ranMax - ranMin + 1

            for i in range(ran):
                print(f'{rows[i][0]}')
                print(f'{rows[i][1]}')

                # 音频
                soundpath = f'{os.getcwd()}\Speech_US'
                soundpath2 = r'\\' + rows[i][0] + r'.mp3'
                soundpath += soundpath2

                playsound(soundpath)

                recation = input('')


        # sys.exit(app.exec_())




print('成功退出')