# -*- coding: utf-8 -*-
#调用有道翻译或百度翻译API的类
import http
from http import client
import urllib
from urllib import parse
from urllib import error
import hashlib
import random
import json

class translationAPI:
    """
    调用有道翻译API或百度翻译API，对文本进行翻译。
    初始化：APItype，ID，密钥，API地址，翻译前语言，翻译后语言

    函数：
       getUrlEncodedData_youdao(self,queryText)
          功能：输入待翻译文本（str)，生成有道翻译API的url编码的数据：myurl。

        getUrlEncodedData_baidu(self,queryText)
          功能：输入待翻译文本（str)，生成百度翻译API的url编码的数据：myurl。

       requestUrl(self,myurl)
          功能：输入url编码数据，向API地址发送请求，获取翻译完成的json格式页面数据：html。

        parserHtml_youdao(self,html)
          功能：输入html，解析有道翻译API页面内容，提取翻译文本。

        parserHtml_baidu(self,html)
          功能：输入html，解析百度翻译API页面内容，提取翻译文本。

        translate(self,querytext)
          功能：执行完整的API调用翻译，返回翻译结果。
    """
    def __init__(self,appKey,secretKey,httpConnection='openapi.youdao.com',APItype='youdao',langFrom='auto',langTo='zh-CHS'):
        """
        API调用参数初始化
        :param appKey: 应用ID
        :param secretKey: 应用密钥
        :param httpConnection: API http地址，默认有道：'openapi.youdao.com'
        :param APItype: 选择API，默认有道：'youdao'，可选百度：'baidu'
        :param langFrom: 待翻译文本语言，参看有道和百度的语言代码列表,默认:'auto'
        :param langTo: 翻译后文本语言，参看有道和百度的语言代码列表，默认有道中文：'zh-CHS'
        """
        self.APItype = APItype #选择调用的API，默认有道翻译'youdao'，可选：百度'baidu'
        self.myurl_youdao = '/api' #有道翻译url开头
        self.myurl_baidu = '/api/trans/vip/translate' #百度翻译url开头
        self.appKey = appKey  #应用id
        self.secretKey = secretKey  #应用密钥
        self.httpConnection = httpConnection  # 翻译API HTTP地址
        self.langFrom = langFrom #翻译前文字语言，默认为'auto',自动检查
        self.langTo = langTo #翻译后文字语言，默认为'auto',自动检查

    def getUrlEncodedData_youdao(self,queryText):
        """
        按照有道翻译API的格式，将数据url编码
        :param queryText: 待翻译的文本
        :return: myurl，url编码过的数据
        """
        if not isinstance(queryText,str) :
            queryText = str(queryText)
        salt = random.randint(1, 65536)
        # 生成字符串sign，做md5加密，注意计算md5之前，sign必须为UTF-8编码
        sign = self.appKey + queryText + str(salt) + self.secretKey
        sign = sign.encode('utf-8')
        m1 = hashlib.md5()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = self.myurl_youdao + '?appKey=' + self.appKey + '&q=' + parse.quote(
            queryText) + '&from=' + self.langFrom + '&to=' + self.langTo + '&salt=' + str(
            salt) + '&sign=' + sign
        return myurl

    def getUrlEncodedData_baidu(self,queryText):
        """
        按照百度翻译API的格式，将数据url编码
        :param queryText: 待翻译的文本
        :return: myurl，url编码过的数据
        """
        if not isinstance(queryText,str):
            queryText = str(queryText)
        salt = random.randint(32768,65536)
        # 生成字符串sign，做md5加密，注意计算md5之前，sign必须为UTF-8编码
        sign = self.appKey + queryText + str(salt) + self.secretKey
        sign = sign.encode('utf-8')
        m1 = hashlib.md5()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = self.myurl_baidu + '?appid=' + self.appKey + '&q=' + parse.quote(
            queryText) + '&from=' + self.langFrom + '&to=' + self.langTo + '&salt=' + str(salt) + '&sign=' + sign
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
            return html
        except error.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except error.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        except Exception as e:
            print(e)

    def parserHtml_youdao(self,html,queryText):
        """
        解析有道翻译页面，输出翻译结果
        :param html: 翻译返回的页面内容，json格式
        :param queryText: 待翻译文本
        :return: outStr，翻译结果
        """
        if not html:
            print('html is empty.')
        try:
            target = json.loads(html)
            key = u'translation'
            if key in target:
                outStr = target["translation"][0]  # 取得翻译后的文本结果，测试可删除注释
            else:
                outStr = queryText  # 翻译失败，返回原文本
            return outStr
        except Exception as e:
            print("Json load Error.")
            print(e)

    def parserHtml_baidu(self,html,queryText):
        """
        解析百度翻译页面，输出翻译结果
        :param html: 翻译返回的页面内容，json格式
        :param queryText: 待翻译文本
        :return: outStr，翻译结果
        """
        if not html:
            print('html is empty.')
        #读取json格式的翻译文本
        try:
            target = json.loads(html)
            key = u'trans_result'
            if key in target:
                outStr = target["trans_result"][0]["dst"]  # 取得翻译后的文本结果，测试可删除注释
            else:
                outStr = queryText  # 返回原文本
            return outStr
        except Exception as e:
                print("Json load Error.")
                print(e)


    def translate(self,querytext):
        if self.APItype == 'youdao':
            myurl = self.getUrlEncodedData_youdao(querytext)
            html = self.requestUrl(myurl)
            result = self.parserHtml_youdao(html,querytext)
            return result
        if self.APItype == 'baidu':
            myurl = self.getUrlEncodedData_baidu(querytext)
            html = self.requestUrl(myurl)
            result = self.parserHtml_baidu(html,querytext)
            return result

def main_youdao():
    """
    测试，调用有道翻译APP
    :return: None
    """
    APItype = 'youdao'
    appKey = '599f38e087d0d26c'  # 应用id
    secretKey = 'Nn6nV6t5kdKvLO4fvS1PJI0lLCze6L76'  # 应用密钥
    langFrom = 'EN'  # 英文
    langTo = 'zh-CHS'  # 中文
    httpConnection = 'openapi.youdao.com'
    #youdao = translationAPI(appKey,secretKey,httpConnection,APItype,langFrom,langTo)
    youdao = translationAPI(appKey,secretKey) #默认调用有道翻译API
    print(youdao.translate('good'))

def main_baidu():
    """
    测试，调用百度翻译APP
    :return: None
    """
    APItype = 'baidu'
    appKey = '20151113000005349'  # 应用id
    secretKey = 'osubCEzlGjzvw8qdQc41'  # 应用密钥
    langFrom = 'en'  # 英文
    langTo = 'zh'  # 中文
    httpConnection = 'api.fanyi.baidu.com'
    baidu = translationAPI(appKey,secretKey,httpConnection,APItype,langFrom,langTo)
    print(baidu.translate('apple'))

if __name__ == '__main__':
    main_youdao()
    #main_baidu()

