import requests

import urllib3.contrib.pyopenssl

urllib3.contrib.pyopenssl.inject_into_urllib3()

from operateExcel import *
from logistTest import *

import numpy as np

# 扇贝网爬虫，获取英语单词
category_res = requests.get('https://www.shanbay.com/api/v1/vocabtest/category/?_=1566889802182', verify=False)
category_json = category_res.json()
category_data = category_json['data']

# 选择出题范围
for i in range(10):
    print(str(i + 1) + '.' + category_data[i][1])
number = int(input('请选择出题范围：'))

url = 'https://www.shanbay.com/api/v1/vocabtest/vocabularies/'
headers = {
    'Referer': 'https://www.shanbay.com/vocabtest/',

}
params = {
    'category': category_data[number - 1][0],
    '_': '1566889452889'
}

res = requests.get(url, headers=headers, params=params, verify=False)
jsonres = res.json()

vacabularies = jsonres['data']

new_ranks=[]
new_pk=[]

new_words=[]

for va in vacabularies:
    new_words.append([va['rank'],va['pk']])

# print(new_words)
new_w = np.array(new_words)

print(LogistPredict(new_w))