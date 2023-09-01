# -*- coding: utf-8 -*-
# @time    : 2023/3/27 21:28
# @author  : w-xin
# @file    : img_reptile.py
# @software: PyCharm

"""
优美图库爬取图片
https://www.umei.cc/weimeitupian/yijingtupian/

思路
页面源代码中提取子页面链接
即需要找到源代码中的 href 标签
"""
import time

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':

    url = 'https://www.umei.cc/weimeitupian/yijingtupian/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    respnd = requests.get(url = url, headers = headers)
    respnd.encoding = 'utf-8'
    html_content = respnd.text

    soup = BeautifulSoup(html_content, 'lxml')
    img_aLi = soup.select('div[class="item_list infinite_scroll"] > div[class="item masonry_brick"] > '
                          'div[class="item_b clearfix"] > div[class="title"] > span > a')

    # 从标签内获取属性的值
    fa_url = 'https://www.umei.cc/'
    for li in img_aLi:
        href = li.get('href')  # 拿到子页面链接
        child_url = fa_url + href.strip('/')
        # print(child_url)

        child_respond = requests.get(url = child_url, headers = headers)
        child_respond.encoding = 'utf-8'
        child_content = child_respond.text

        # 从子页面拿到图片下载路径
        # 通过 BeautifulSoup 拿到图片下载地址
        child_soup = BeautifulSoup(child_content, 'lxml')
        child_url = child_soup.find('div', class_ = "big-pic").find('a').find('img').get('src')
        # print(child_url)

        # 下载图片
        img_respond = requests.get(child_url)
        # 从响应里面拿到图片
        img_respond.content  # 这里拿到的是字节  要把字节写到文件里面去
        # 文件命名  建立文件夹存储
        img_name = child_url.split('/')[-1]
        with open('./img/' + img_name, mode = 'wb') as f:
            f.write(img_respond.content)  # 图片内容写入文件

        print(f'{img_name} over')
        time.sleep(1)

    print('all over!')

    respnd.close()
    child_respond.close()



    # print(href)