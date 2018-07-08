#-*- coding: utf-8 -*-
"""调用百度翻译API，对Excel文档的英文摘要进行翻译
   函数：
         translate_e2z(inputfile,outputfile)
         功能：输入文档，调用百度翻译API，英译中，输出文档
"""
import http
from http import client
import hashlib
import urllib.request
from urllib import parse
import urllib.error
import random
import json
import pandas as pd

def translate_e2z(text):
    """当输入为文本文件时，使用translate_e2z(inputfile,outfile);text为某一段文本"""
     #fin = open(inputfile,'r') #当inputfile是文件时使用，读取文件
     #fout = open(outfile,'w') #当outputfile是文件时使用，写入文件
    translated = ""
    doc = str(text).split(". ")
    for eachline in doc: #doc为一段文本
        #appid = '20180520000163053'
        #secreKey = 'rnE7cs0NwY9gQfNsTSZF'
        appid = ''
        secreKey = ''
        myurl = '/api/trans/vip/translate'
        #q = eachline.strip() #当inputfile时，文本中每一行作为一个翻译源
        q = eachline.strip()+"." #当text时，文本中每一行作为一个翻译源，再加上"."句号
        fromLang = 'en' #英文
        toLang = 'zh' #中文
        salt = random.randint(32768,65536)
        sign = appid+q+str(salt)+secreKey
        sign = sign.encode('UTF-8')
        m1 = hashlib.md5()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET',myurl)
            #response是HTTPResponse对象
            response = httpClient.getresponse()
        except urllib.error.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ',e.code)
        except urllib.error.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ',e.reason)
        except Exception as e:
            print('translate error.')
            print(e)
            continue
        html = response.read().decode('UTF-8')
        try:
            target2 = json.loads(html)
        except Exception as e:
            print("loads Json error")
            print(e)
            continue

        key = u'trans_result'
        if key in target2:
            src = target2["trans_result"][0]["dst"] #取得翻译后的文本结果，测试可删除注释
            outStr = src
        else:
            outStr = eachline
        #将翻译结果保存在list里，并返回该list
        try:
            translated += outStr.strip()
        except Exception as e:
            print("String error")
            print(e)
            continue
        #fout.write(outStr.strip()+'\n')
    #fin.close()
    #fout.close()
    #print('翻译 成功')
    return translated



if __name__ == '__main__':
    #inputfile = 'E:/python/Multi_translate/input/test.txt'
    #outputfile = 'E:/python/Multi_translate/output/tr_test.txt'
    #translate_e2z(inputfile,outputfile)
    df = pd.read_excel('E:/python/Multi_translate/input/MSCP1626.xlsx')
    df['translated_AB'] = None
    num = 0
    for doc in df.ix[:,5]:
        df['translated_AB'][num] = translate_e2z(doc)
        num += 1
    try:
        df.to_excel(u'E:/python/Multi_translate/output/TR_MSCP1626.xlsx')
    except Exception as e:
        print("to_excel error")
        print(e)
    print('the num of valid docs is : %s' % num)
    print('---' * 20)
