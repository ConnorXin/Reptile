# -*- coding: utf-8 -*-
# @time    : 2023/4/5 20:53
# @author  : w-xin
# @file    : CombineTraining_CloudComment.py
# @software: PyCharm

"""
网易云音乐评论爬取    https://music.163.com/

通过评论在网页源代码中查找发现
网页源代码并不能搜到 框架源代码也不能搜到

1 找到未加密的参数
2 想办法把参数进行加密 必须参考网易的逻辑  params, encSecKey
3 请求到网易 拿到评论信息
"""
import json
from base64 import b64encode

import requests
from Cryptodome.Cipher import AES


def get_encSecKey():
    '''

    :return: 固定的 ensSecKey
    '''

    return "be4d5c02808612eb205bb6d9f7531d871330f03067b1aa453ddc1652fb88a051f2264ee29dee736acd39899ebec1c501a59ee09cfe2ab4974fe4e5881ae6543783215d570b7bfd5c3be4e152766d1a86b792ae5962e37d612ab21bc33ecc19bbe03339878550cd443c31a2f82b8ff49f5dc47929e2c00713fd0751bccad97398"


def to_16(data):
    '''
    把数据拉长为16位
    :param data: 数据参数
    :return: 拉长后的数据参数
    '''
    pad = 16 - len(data) % 16
    data += chr(pad) * pad

    return data


def get_params(data):
    '''
    把下方的 d 还原  得到两次加密过程
    :param data: 网易评论的参数  为字符串
    :return: 两次加密的结果
    '''
    # 第一次加密
    first = enc_params(data, g)
    # 第二次加密
    second = enc_params(first, i)

    return second


def enc_params(data, key):
    '''
    把下方的 b 还原  即加密过程
    :param data: 网易数据的评论参数
    :param key: 密钥
    :return: 加密后的结果
    '''
    iv = '0102030405060708'
    data = to_16(data)
    aes = AES.new(key = key.encode('utf-8'), IV = iv.encode('utf-8'), mode = AES.MODE_CBC)  # 创造加密器
    bs = aes.encrypt(data.encode('utf-8'))  # 加密
    return str(b64encode(bs), 'utf-8')


if __name__ == '__main__':

    # 在开发者工具 xhr 中找到评论的 url
    requests_url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
    # 请求方式是 POST
    # 通过抓包工具知道 window.asrsea 是加密的工具
    # 而真实的参数就是下面的 i0x
    data = {
        'csrf_token': '',
        'cursor': '-1',
        'offset': '0',
        'orderType': '1',
        'pageNo': '1',
        'pageSize': '20',
        'rid': 'R_SO_4_1951069525',
        'threadId': 'R_SO_4_1951069525'
    }

    # data 转化为字符串
    data = json.dumps(data)
    # 处理加密过程
    # window.asrsea 源头是 d
    ''' 加密过程
        function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {  d: 数据; e: bsg8Y(["流泪", "强"]) / '010001'; f: '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
                              g: '0CoJUm6Qyw8W8jud' 
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),  需要把 i 定死 不能变
        h
    }
    '''
    # 参数准备
    e = '010001'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    g = '0CoJUm6Qyw8W8jud'
    i = 'INoCHwJSELpR0wCX'


    respond = requests.post(url = requests_url, data = {
                'params': get_params(data),
                'encSecKey': get_encSecKey()
            })

    print(respond.text)


    respond.close()