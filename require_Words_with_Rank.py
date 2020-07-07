#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple
import requests

import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

from operateExcel import *

#扇贝网爬虫，获取英语单词
category_res=requests.get('https://www.shanbay.com/api/v1/vocabtest/category/?_=1566889802182',verify=False)
category_json=category_res.json()
category_data=category_json['data']

#选择出题范围
for i in range(10):
    print(str(i+1)+'.'+category_data[i][1])
number=int(input('请选择出题范围：'))

url='https://www.shanbay.com/api/v1/vocabtest/vocabularies/'
headers={
    'Referer': 'https://www.shanbay.com/vocabtest/',

    }
params={
    'category':category_data[number-1][0],
    '_': '1566889452889'
    }

res=requests.get(url,headers=headers,params=params,verify=False)
jsonres=res.json()

vacabularies=jsonres['data']
knows=[]
unknows=[]
print()
print('以下单词你是否认识？')
n=0
z=0

b=open('错词本.txt','a+')
b.write('你不认识的单词有：\n')

print(vacabularies)
#测试开始，挑选认识的单词
for vacabulary in vacabularies:
    n=n+1
    vacabu=vacabulary['content']
    print('第'+str(n)+'个：'+vacabu)
    # print(f'rank={vacabulary["rank"]},pk={vacabulary["pk"]}')
    # print('-'*50)
    index=vacabularies.index(vacabulary)
    for d in vacabulary["definition_choices"]:
        if d['rank']==vacabulary['rank']:
            translation=d['definition']
    while True:
        judge=input('认识选Y，不认识选N：')
        if judge=='Y':
            value=[vacabu, translation, f'{vacabulary["rank"]}',f'{vacabulary["pk"]}', '1', '0']
            print(value)
            update_note_xls('的错词本.xls', value,1)
            knows.append(index)
            break
        elif judge=='N':
            update_note_xls('的错词本.xls',[vacabu,translation,f'{vacabulary["rank"]}',f'{vacabulary["pk"]}','0','0'],0)
            unknows.append(index)

            z=z+1
            b.write(str(z)+'.'+vacabu+'\n')
            break
        else:
            print('请输入Y或者N')

print(f'v={vacabularies}')



print()
print('测试结束，以下是测试结果：')
print('认识'+str(len(knows))+'个单词，不认识'+str(len(unknows))+'个单词。')
print('你可真棒！')
print()

right=[]
wrong=[]

#选择正确的词义
b.write('你记错的单词有：\n')
m=0
print(len(knows))
for know in knows:
    vacabulary_know=vacabularies[know]
    word=vacabulary_know['content']
    print()
    print(word)

    definitions=vacabulary_know['definition_choices']

    for i in range(4):
        print(str(i+1)+'.'+definitions[i]['definition'])
    choice=int(input('单词测试，请选择正确的词义：'))
    rank=definitions[choice-1]['rank']
    if rank==vacabulary_know['rank']:
        right.append(word)
    else:
        wrong.append(word)
        m=m+1
        b.write(str(m)+'.'+word+'\n')

print()
print('测试结果出来啦！')

print('认识的单词里掌握了这几个：')
print(right)
print()
print('没掌握的是这几个：')
print(wrong)