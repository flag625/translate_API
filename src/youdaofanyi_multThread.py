#!/urs/bin/env python
# -*- coding: utf-8 -*-

from http import client
from urllib import parse
from urllib import error
import hashlib
import random
import json
import pandas as pd
import numpy as np
import threading
from time import ctime, sleep

class youdaofanyi(object):
    """
    调用有道翻译API，对文本进行翻译。
    初始化：APItype，ID，密钥，API地址，翻译前语言，翻译后语言

    函数：
    getUrlEncodedData(self, queryText)
    功能：输入待翻译文本（str)，生成有道翻译API的url编码的数据：myurl。

    requestUrl(self, myurl)
    功能：输入url编码数据，向API地址发送请求，获取翻译完成的json格式页面数据：html。

    parserHtml_youdao(self, html)
    功能：输入html，解析有道翻译API页面内容，提取翻译文本。

    translate(self, querytext)
    功能：执行完整的API调用翻译，返回翻译结果。
    """

    def __init__(self,appKey,secretKey,httpConnection='openapi.youdao.com',
                langFrom='auto',langTo='zh-CHS'):
        self.myurl_youdao = '/api'  # 有道翻译url开头
        self.appKey = appKey  # 应用id
        self.secretKey = secretKey  # 应用密钥
        self.httpConnection = httpConnection  # 翻译API HTTP地址
        self.langFrom = langFrom  # 翻译前文字语言，默认为'auto',自动检查
        self.langTo = langTo  # 翻译后文字语言，默认为'auto',自动检查
        self.df_res = pd.DataFrame()

    def getUrlEncodedData(self, queryTest):
        """
                按照有道翻译API的格式，将数据url编码
                :param queryText: 待翻译的文本
                :return: myurl，url编码过的数据
        """
        if not isinstance(queryTest, str):
            queryTest = str(queryTest)
        salt = random.randint(1, 65536)
        # 生成字符串sign，做md5加密，注意计算md5之前，sign必须为UTF-8编码
        sign = self.appKey + queryTest + str(salt) + self.secretKey
        sign = sign.encode('utf-8')
        m1 = hashlib.md5()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = self.myurl_youdao + '?appKey=' + self.appKey + '&q=' + parse.quote(
            queryTest) + '&from=' + self.langFrom + '&to=' + self.langTo + '&salt=' + str(
            salt) + '&sign=' + sign
        #print(myurl)
        return myurl

    def requestUrl(self,myurl):
        """
        发送翻译请求，获得翻译页面
        :param myurl: url编码数据
        :return: html，翻译页面
        """
        try:
            httpClient = client.HTTPConnection(self.httpConnection)
            httpClient.request('GET', myurl)
            # response是HTTPResponse对象
            response = httpClient.getresponse()
            html = response.read().decode('utf-8')
            #print('html: '+html)
            return html
        except error.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except error.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        except Exception as e:
            print(e)

    def parserHtml(self,html,queryTest):
        """
        解析有道翻译页面，输出翻译结果
        :param html: 翻译返回的页面内容，json格式
        :param queryText: 待翻译文本
        :return: outStr，翻译结果
        """
        if not html:
            print("翻译失败：html is empty！")
        try:
            target = json.loads(html)
            key = u'translation'
            if key in target:
                outStr = target["translation"][0]  # 取得翻译后的文本结果，测试可删除注释
                print("翻译成功。")
            else:
                outStr = queryTest  # 翻译失败，返回原文本
                print("翻译失败，返回原文！")
            return outStr
        except Exception as e:
            print("Json load Error.")
            print(e)

    def __call__(self, i, df):
        if df.empty:
            print("没有数据，返回原值！")
        else:
            print("Part %d begin to translate at %s" %(i,ctime()))
            for j, doc in enumerate(df.iloc[:,5]):
                if not isinstance(doc,str):
                    continue
                else:
                    #print("原文：%s" %doc)
                    myurl = self.getUrlEncodedData(doc)
                    #print("myurl："+myurl)
                    html = self.requestUrl(myurl)
                    #print("html："+html)
                    result = self.parserHtml(html, doc)
                    #print("译文："+result)
                    df['translated_AB'][j] = result
                    print("Part %d row %d translate done." %(i,j))
                    sleep(0.1)
            print("Part %d Done: %s" %(i,ctime()))
            #print(df.iloc[:,6])

        self.df_res = df
        #print(result)
        #return result


'''
    def translate(self,querytext):
        myurl = self.getUrlEncodedData(querytext)
        html = self.requestUrl(myurl)
        result = self.parserHtml(html,querytext)
        return result
'''

#将Excel文档转化为queryText，同时实现分块。
def Excel2queryText(path, split=1):
    """
    读取Excel内容，转化为dataframe，均分成几个小dataframe
    :param path: Excel所在路径
    :param split: 均分的数量
    :return: 带有均分后的df的列表
    """
    df = pd.DataFrame()
    try:
        df = pd.read_excel(path) #读取Excel
    except Exception as e:
        print(e)
        raise e

    if df.empty:
        print("Excel 文本为空！")
        return

    df['translated_AB'] = None
    df_list = []
    row_total = len(df)

    if row_total < split or split < 0:
        print("均分数无效，执行默认值 1 ！")
        return Excel2queryText(path)
    else:
        dif = int(row_total / split)
        if row_total % split != 0:
            for i in range(split - 1):
                df_p = df.iloc[(dif * i):dif * (i + 1), :].reset_index(drop=True)
                df_list.append(df_p)
            df_l = df.iloc[(dif * (split - 1)):, :].reset_index(drop=True)
            df_list.append(df_l)
        else:
            for i in range(split):
                df_p = df.iloc[(dif * i):dif * (i + 1), :].reset_index(drop=True)
                df_list.append(df_p)

        return df_list

#合并结果集
def merge2Excel(path, df_list):
    if not df_list:
        print("没有 DataFrame 列表结果!")
    df = pd.concat(df_list)
    try:
        df.to_excel(path) #输出到Excel
    except Exception as e:
        print(e)

#例子
def example_fanyi(df_list):
    kwargs = {"appKey":'apiID',
              "secretKey":"密码"}
    #text = ["To the world you may be one person, but to one person you may be the world.",
            #"No man or woman is worth your tears, and the one who is, won't make you cry."]
    num = len(df_list)
    fanyi = []
    threads = []
    for i in range(num):
        f = youdaofanyi(**kwargs)
        fanyi.append(f)

    for i, df in enumerate(df_list):
        t = threading.Thread(target=fanyi[i](i, df))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return [f.df_res for f in fanyi]
    #只返回第一个，其余的没有返回。

#test
if __name__ == "__main__":
    #example_fanyi()
    df_list = Excel2queryText('/Users/cloudin/PycharmProjects/translate_API/input/test.xlsx',3)
    res_list = example_fanyi(df_list)
    merge2Excel('/Users/cloudin/PycharmProjects/translate_API/output/test20180718.xlsx',res_list)
    # for i, df in enumerate(df_list):
    #     print("Part %d :" %i)
    #     print(df)
    #     print('\n')

