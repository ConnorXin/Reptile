# -*- coding: utf-8 -*-
'''
movies_dytt.py
电影天堂  https://www.dytt89.com/
获取2023年必看热片片名与下载地址

思路
1 定位到2023必看热片
2 从2023必看热片中提取到子页面的链接地址
3 请求子页面的链接地址 拿到下载地址
'''

import numpy as np
import pandas as pd
import requests
import re


if __name__ == '__main__':

    url = 'https://www.dytt89.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    respond = requests.get(url = url, headers = headers)  # verify = False  意思是去掉安全验证
    respond.encoding = 'gb2312'  # 指定字符集
    page_content = respond.text  # 指定字符集之后正常显示中文

    # print(page_content)  # 乱码，requests 里面默认解码是 utf-8；网站编码若不是 utf-8，则出错


    # 使用 "2023必看热片" 进行定位
    # 解析数据
    obj1 = re.compile(r'2023必看热片.*?<ul>(?P<moive_li>.*?)</ul>', re.S)
    obj2 = re.compile(r'a href=\'(?P<moive_url>.*?)\' title=', re.S)
    obj3 = re.compile(r'◎译　　名(?P<translate_name>.*?)<br />◎片　　名(?P<name>.*?)<br />.*?'
                      r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<download>.*?)">magnet:?', re.S)
    movieLi = obj1.finditer(page_content)
    for it in movieLi:
        movie_2023 = it.group('moive_li')

        # 提取 movie_2023 子页面中的 a 标签里面的 herf 超链接  即子页面的链接
        childUrl = obj2.finditer(movie_2023)
        child_urlList = np.array([])
        for itt in childUrl:
            # movie_url =
            # 拼接子页面的 url
            child_urlList = np.append(child_urlList, url + itt.group('moive_url').strip('/'))

            # print(movie_2023)
        # print(child_urlList)

    # 从子页面解析数据
    translate_name = np.array([])
    movie_name = np.array([])
    movie_download = np.array([])
    movies_download = pd.DataFrame(columns = ['Translate Name', 'Movie Name', 'Download'])
    for ur in child_urlList:
        child_respond =requests.get(url = ur, headers = headers)
        child_respond.encoding = 'gb2312'
        child_content = child_respond.text
        child_contents = obj3.search(child_content)
        translate_name = child_contents.group('translate_name').strip()
        movie_name = child_contents.group('name').strip()
        movie_download = child_contents.group('download').strip()

        movies_download = movies_download.append({
            'Translate Name': translate_name,
            'Movie Name': movie_name,
            'Download': movie_download
        }, ignore_index=True)

    # print(translate_name)
    # print(movie_name)
    print(movies_download)

    respond.close()
    child_respond.close()


    movies_download.to_csv('dyttMovie_2023.csv', encoding = 'utf-8')