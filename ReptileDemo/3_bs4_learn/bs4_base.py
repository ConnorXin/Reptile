# -*- coding: utf-8 -*-
# @time    : 2023/3/27 20:35
# @author  : w-xin
# @file    : bs4_base.py
# @software: PyCharm

"""
北京新发地 爬取农贸产品的价格
但是现在的北京新发地网址已经不是 GET 请求
如下代码仅供 bs4.BeautifulSoup 学习
"""

import time
import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':

    url = 'http://www.xinfadi.com.cn/index.html'
    respond = requests.get(url)

    # 解析数据
    # 把页面源代码交给 BeautifulSoup 进行处理，生成 bs 对象
    page = BeautifulSoup(respond.text, 'html.parser')  # html.parser 指定 html 解析器

    # 从 bs 对象中查找数据
    '''
    find(标签, 属性=值)
    find_all(标签, 属性=值)
    '''
    table = page.find('table', class_ = 'hq_table')  # class 是关键字 因此在后面添加下划线
    table = page.find('table', attrs = {'class': 'hq_table'})  # 与上一行一个意思不同写法 可以避免 class

    # 拿到所有数据行
    trs = table.find_all('td')[1: ]
    for tr in trs:
        tds = tr.find_all('td')
        name = tds[0].text
        low = tds[1].text
        avg = tds[2].text
        high = tds[3].text
        scale = tds[4].text
        kind = tds[5].text
        date = tds[6].text

    time.sleep(1)
