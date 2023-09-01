# -*- coding: utf-8 -*-
# @time    : 2023/6/19 13:14
# @author  : w-xin
# @file    : example_withThreadProcessPool.py
# @software: PyCharm

"""
北京新发地 网站

1 如何提取单个页面数据
2 线程池 多个页面同时抓取
"""
import requests
import csv
from lxml import etree
from concurrent.futures import ThreadPoolExecutor


def download_one_page(url):
    '''
    提取一个页面的数据
    :param url: 页面网址
    :return:
    '''
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    html = etree.HTML(resp.text)
    table = html.xpath('//*[@id="table"]')[0]
    trs = table.xpath('./tr')[1:-1]  # 剔除表头
    # trs = table.xpath('./tr[position()>1]')

    # 遍历每个 tr
    for tr in trs:
        txt = tr.xpath('./td/text()')
        # 对数据做简单的处理 例如 / \\
        txt = (item.strip() for item in txt)  # 迭代器
        # 数据写入
        csvwriter.writerow(txt)
        # print(list(txt))
    print(f'{url} complete.')
    # print(trs)


if __name__ == '__main__':

    f = open('foreign exchange data.csv', mode = 'w', encoding = 'gbk')
    csvwriter = csv.writer(f)
    # for i in range(1, 14870):   # page 14870  效率很低
    #     download_one_page(f'http://www.xinfadi.com.cn/marketanalysis/0/list/{i}.shtml')
    # download_one_page('http://www.waihuipaijia.cn/helandun.htm')

    contries = ['aomenyuan', 'helandun', 'hanguoyuan', 'feilvbinbisuo', 'xinxilanyuan', 'ruidiankelang',
           'yidalilila', 'danmaikelang', 'fenlanmake', 'faguofalang', 'deguomake']
    # 使用线程池
    with ThreadPoolExecutor(5) as t:  # 同时50个页面进行下载
        for i in range(10):
            t.submit(download_one_page(f'http://www.waihuipaijia.cn/{contries[i]}.htm'))

    print('All Complete.')