#/usr/bin/env python
#coding:utf-8
 
import http
from http import client
import hashlib
import urllib.request
from urllib import parse
import urllib.error
import random
import json

appid = '2015111300000534'
secretKey = 'osubCEzlGjzvw8qdQc4'

 
httpClient = None
myurl = '/api/trans/vip/translate'
q = 'apple'
fromLang = 'en'
toLang = 'zh'
salt = random.randint(32768, 65536)

sign = appid+q+str(salt)+secretKey
sign = sign.encode('utf-8')
m1 = hashlib.md5()
m1.update(sign)
sign = m1.hexdigest()
myurl = myurl+'?appid='+appid+'&q='+parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
 
try:
    httpClient = client.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('GET', myurl)
 
    #response是HTTPResponse对象
    response = httpClient.getresponse()
    print(response.read())
except Exception as e:
    print(e)
finally:
    if httpClient:
        httpClient.close()
