# -*- coding: utf-8 -*-
# @time    : 2023/3/30 14:21
# @author  : w-xin
# @file    : zbjWebsite.py
# @software: PyCharm

"""
猪八戒网站
https://beijing.zbj.com/
"""


import time
import requests
from lxml import etree

if __name__ == '__main__':

    url = 'https://beijing.zbj.com/search/service/?kw=saas&r=2'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }

    html_respond = requests.get(url = url, headers = header)
    html_content = html_respond.text
    # print(html_content)

    # xpath 解析
    tree = etree.HTML(html_content)
    bricks = tree.xpath('//*[@id="__layout"]/div/div[3]/div/div[4]/div/div[2]/div[1]/div')  # 全部服务商
    # print(brick)

    # 遍历每一个服务商
    for brick in bricks:
        server_name = brick.xpath('.//div/a/div[2]/div[1]/div/text()')
        server_price = brick.xpath('.//div/div[2]/div[1]/span/text()')
        server_intro = brick.xpath('.//div/div[2]/div[2]/a/text()')


        # print(server_name)
        print(server_price)
        # print(server_intro)
        time.sleep(1)
    html_respond.close()
