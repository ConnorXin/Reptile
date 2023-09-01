# -*- coding: utf-8 -*-
'''
movies_doubanTOP250.py
豆瓣电影 TOP250  https://movie.douban.com/top250
网页源代码能够找到电影相关信息 说明是服务器渲染的数据

思路
1 拿到网页源代码  通过 requests 模块
2 提取有效信息  通过 re 模块
'''

import numpy as np
import pandas as pd
import requests
import re


if __name__ == '__main__':

    url = 'https://movie.douban.com/top250'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    respond = requests.get(url, headers = headers)
    page_content = respond.text  # 发现为空 必须要有 User-Agent


    '''
    想要排行中的 电影名字 年份 评分 评价数
    '''
    movies = pd.DataFrame(columns=['name', 'year', 'rating', 'ratingNum'])
    # 解析数据
    obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<movie_name>.*?)</span>'
                     r'.*?<p class="">.*?<br>(?P<movie_year>.*?)&nbsp;/&nbsp'
                     r'.*?<span class="rating_num" property="v:average">(?P<movie_rate>.*?)</span>'
                     r'.*?<span>(?P<movie_rateNum>.*?)人评价</span>', re.S)
    movie_info = obj.finditer(page_content)
    for it in movie_info:

        name = np.array(it.group('movie_name'))  # 成功拿到数据
        year = np.array(it.group('movie_year').strip())  # 年份前面有好多空白 使用 strip 处理
        rating = np.array(it.group('movie_rate'))
        ratingNum = np.array(it.group('movie_rateNum'))

        movies = movies.append({
            'name': name, 'year': year,
            'rating': rating, 'ratingNum': ratingNum
        }, ignore_index=True)



    respond.close()


    movies.to_csv('movies_doubanTOP250.csv', encoding = 'utf-8')



    print(movies)
