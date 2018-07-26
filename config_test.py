# -*- coding: utf-8 -*-
import configparser
import random
import hashlib

config = configparser.ConfigParser()
config.read('/Users/cloudin/PycharmProjects/translate_API/api.conf')
from urllib import parse


def getUrlEncodedData(queryTest):
    """
            按照有道翻译API的格式，将数据url编码
            :param queryText: 待翻译的文本
            :return: myurl，url编码过的数据
    """

    try:
        appKey = config.get('youdaoLZX_config', 'appKey')
        print(appKey)
        secretKey = config.get('youdaoLZX_config', 'appKey')
        print(secretKey)
    except Exception as e:
        raise e


    if not isinstance(queryTest, str):
        queryTest = str(queryTest)
    salt = random.randint(1, 65536)
    # 生成字符串sign，做md5加密，注意计算md5之前，sign必须为UTF-8编码
    sign = appKey + queryTest + str(salt) + secretKey
    sign = sign.encode('utf-8')
    m1 = hashlib.md5()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = '/api' + '?appKey=' + appKey + '&q=' + parse.quote(
        queryTest) + '&from=' + 'En' + '&to=' + 'ch' + '&salt=' + str(
        salt) + '&sign=' + sign
    print(myurl)
    #return myurl

    if __name__ == '__main__':
        getUrlEncodedData('a')