# /usr/bin/env python
# coding=utf8

import http
from http import client
import hashlib
from hashlib import md5
import urllib
import urllib.request
from urllib import parse
from urllib import error
import random
import json

appKey = '599f38e087d0d26'
secretKey = 'Nn6nV6t5kdKvLO4fvS1PJI0lLCze6L6'

httpClient = None
myurl = '/api'
q = 'good'
fromLang = 'EN'
toLang = 'zh-CHS'
salt = random.randint(1, 65536)

sign = appKey + q + str(salt) + secretKey
sign = sign.encode('utf-8')
m1 = md5()
m1.update(sign)
sign = m1.hexdigest()
myurl = myurl + '?appKey=' + appKey + '&q=' + parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

try:
    httpClient = client.HTTPConnection('openapi.youdao.com')
    httpClient.request('GET', myurl)

    # response是HTTPResponse对象
    response = httpClient.getresponse()
    print(response.read().decode('UTF-8'))

    # 提取翻译结果
    html = response.read().decode('utf-8')
    data = json.loads(html)
    key = u'translation'
    if key in data:
        src = data["translation"][0]  # 取得翻译后的文本结果，测试可删除注释
        outStr = src
    else:
        outStr = q
    print(outStr)

except error.HTTPError as e:
    print('The server couldn\'t fulfill the request.')
    print('Error code: ', e.code)
except error.URLError as e:
    print('We failed to reach a server.')
    print('Reason: ', e.reason)
except Exception as e:
    print(e)
#finally:
#    if httpClient:
#        httpClient.close()

