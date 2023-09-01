# -*- coding: utf-8 -*-
# @time    : 2023/8/19 19:47
# @author  : w-xin
# @file    : 3_blobVideo.py
# @software: PyCharm

"""
blob 加密视频
"""

import requests


if __name__ == '__main__':

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }

    url = 'https://www.iqiyi.com/fc71a21e-c771-47d4-ad79-cfe704ba5d4f'
    response = requests.get(url = url, headers = header)
    print(response.text)
    response.close()






