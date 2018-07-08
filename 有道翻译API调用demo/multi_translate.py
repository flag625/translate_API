# -*- coding: utf-8 -*-
"""调用有道翻译API，对Excel文档的英文摘要进行翻译
   函数：
         translate_e2z(inputfile,outputfile)
             功能：输入文档，调用有道翻译API，英译中，输出文档
         translate_e2z(text)
             功能：输入文本，调用有道翻译API，英译中，输出翻译好的文本
"""
import http
from http import client
import hashlib
from hashlib import md5
import urllib.request
from urllib import parse
from urllib import error
import random
import json

import pandas as pd
from pandas import DataFrame

def translate_e2z(text):
    """输入文档，调用有道翻译API，英译中，输出文档"""
    #API参数设置
    appKey = '599f38e087d0d26'
    secretKey = 'Nn6nV6t5kdKvLO4fvS1PJI0lLCze6L7'
    httpClient = None
    myurl = '/api'
    #q = ''
    fromLang = 'EN'
    toLang = 'zh-CHS'
    #salt = random.randint(1, 65536)

    #执行调用
    translated = ""
    doc = str(text).split(". ")
    for line in doc: #读取文本的每一句话
        q = line.strip()+'.' #因为使用句号将tex切分成一句一句，每一句作为一个翻译源，需要补加上"."句号
        salt = random.randint(1,65536)
        # 生成字符串sign，做md5加密，注意计算md5之前，sign必须为UTF-8编码
        sign = appKey + q + str(salt) + secretKey
        sign = sign.encode('utf-8')
        m1 = md5()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = myurl + '?appKey=' + appKey + '&q=' + parse.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
            salt) + '&sign=' + sign
        try:
            httpClient = client.HTTPConnection('openapi.youdao.com')
            httpClient.request('GET', myurl)
            # response是HTTPResponse对象
            response = httpClient.getresponse()
        except error.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except error.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        except Exception as e:
            print(e)
            continue
        finally:
            if httpClient:
                httpClient.close()
        html = response.read().decode('utf-8')
        #汇总翻译结果：
        try:
            target2 = json.loads(html)
        except Exception as e:
            print("loads Json error")
            print(e)
            continue

        key = u'translation'
        if key in target2:
            src = target2["translation"][0]  # 取得翻译后的文本结果，测试可删除注释
            outStr = src
        else:
            outStr = q
        # 将翻译结果保存在list里，并返回该list
        try:
            translated += outStr.strip()
        except Exception as e:
            print("String error")
            print(e)
            continue

    return translated


if __name__ == '__main__':
    df = DataFrame()
    try:
        df = pd.read_excel('E:/python/Multi_translate/input/test.xlsx') #读取Excel
    except Exception as e:
        print(e)
    df['translated_AB'] = None
    num = 0
    for doc in df.ix[:,5]:
        df['translated_AB'][num] = translate_e2z(doc)
        num += 1
        print("translate done: %d" %num)
    try:
        df.to_excel('E:/python/Multi_translate/output/tr_test.xlsx') #输出到Excel
    except Exception as e:
        print(e)
    print('the num of valid docs is : %s' % num)
    print('---' * 20)

