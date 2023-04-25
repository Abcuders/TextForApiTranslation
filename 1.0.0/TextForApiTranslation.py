#!/usr/bin/python3
#coding:utf-8
from json import loads
from requests import post
from ast import literal_eval
from time import sleep

def PostApi(key):#Post Api
    ApiKey = '输入你的小牛ApiKey'
    url = 'https://api.niutrans.com/NiuTransServer/translation'
    date = {'src_text':key,'from':'auto','to':'zh','apikey':ApiKey}#ApiKEY
    ApiDate = post(url,date)
    #print(ApiDate.text)
    if ApiDate.status_code == 200:
        sleep(0.05)
        return literal_eval(ApiDate.text)['tgt_text']

def TextSegment(DateKeys):#文本分段
    i = len(DateKeys)
    Keys = ''
    Dkeys = []
    for i in range(i):
        Keys = Keys + DateKeys[i].replace('\n','^C^') + '\n'
        if len(Keys) < 4500:
            Keys1 = Keys
        else :
            Keys = ''
            Keys = Keys + DateKeys[i].replace('\n','^C^') + '\n'
            Dkeys.append(Keys1.strip('\n'))
    return Dkeys

def ReadTransFile():#读取
    with open(f"{Path}\ManualTransFile.json",'r',encoding='utf-8') as ff:
        return loads(ff.read())

def WriteTransFile(json):#写入
    with open(f'{Path}\TrsData.json','w+',encoding='utf-8') as ff:
        ff.write(str(json))

def DealWithApiDate(Date):#处理数据
    DateKeys = list(Date.keys())
    text = ''
    DateKeysS = TextSegment(DateKeys)#分段以进行加速翻译避免QPS超标
    for i in range(len(DateKeysS)):
        print(f'[i]正在进行{len(DateKeysS)}个分段中的{i+1}')
        text = text + (PostApi(DateKeysS[i]))
    text = text.split('\n')
    for i in range(len(text)):
        Date[DateKeys[i]] = text[i].replace('^C^','\n')
    WriteTransFile(Date)
    print('[i]all ok')

if __name__ == '__main__' :
    Path = input('[in]请输入存在ManualTransFile.json的目录路径>>')
    DealWithApiDate(ReadTransFile())
