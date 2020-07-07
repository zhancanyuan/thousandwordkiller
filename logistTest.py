# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import os

import pandas as pd


def LogistPredict(my_path, vaca):
    # 数据是否要标准化
    scale = False

    # path = f'{os.getcwd()}\David的错词本.xls'
    path = my_path

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
    # plt.show()

    modelLR = LogisticRegression()

    modelLR.fit(x_data, y_data2)

    b = modelLR.coef_
    a = modelLR.intercept_

    pred_y = 1 / (1 + np.exp(-(a + b * x_data)))

    # print(modelLR.predict_proba(x_data[i].reshape(1,-1)))
    print(modelLR.predict(x_data))  # 新测试集

    tmp = modelLR.predict(vaca).tolist()
    c = 0
    result = []
    for i in tmp:
        if i == 0:
            result.append(c)
        c += 1

    return result


if __name__ == "__main__":
    pass
