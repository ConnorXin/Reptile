# -*- coding: utf-8 -*-
# @time    : 2023/3/28 8:32
# @author  : w-xin
# @file    : bs4_select.py
# @software: PyCharm

# 全局取消证书验证
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

import requests
import bs4
import pandas as pd
import time


if __name__ == '__main__':


    # 模拟浏览器头部
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }


    df = pd.DataFrame(columns=['小区名称', '户型', '详细地址', '面积', '价格', '楼层', '朝向', '租用类型'])

    page = 1
    item_num, max_num = 1, 3000  # 爬取3000条数据
    while True:
        # 获取其中一页的源代码
        url = 'https://sz.zu.anjuke.com/fangyuan/p{}/'.format(page)
        response = requests.get(url, headers=header)
        if response.status_code != 200:
            print('终止页为', page)
            break
        response.encoding = 'utf-8'
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        # div_li_1 = soup.select('div[class="zu-info"]')
        # div_li_2 = soup.select('div[class="zu-side"]')
        div_li = soup.select('div[class="zu-itemmod"]')
        print(div_li)

        for div in div_li:
            # 爬取楼层
            flo = div.select('div[class="zu-info"] > p[class="details-item tag"]')[0].text
            flo = flo.split('|')[2]
            flo_ind = flo.find(')')
            flo = flo[: flo_ind + 1]
            # 爬取小区名称
            name = div.select('div[class="zu-info"] > address[class="details-item"] > a[target="_blank"]')[0].text
            # 爬取户型
            sha_1 = div.select('div[class="zu-info"] > p[class="details-item tag"] > b[class="strongbox"]')[0].text
            sha_2 = div.select('div[class="zu-info"] > p[class="details-item tag"] > b[class="strongbox"]')[1].text
            hou_shape = sha_1 + '室' + sha_2 + '厅'
            # 爬取地址
            address_ = div.select('div[class="zu-info"] > address[class="details-item"]')[0].text
            address_ = address_.replace(' ', '')
            address_ = address_.strip()
            for i in range(1, 50):
                if len(address_[0: i]) == len(name):
                    address_ = address_[i:]
                    address_ = address_.strip()
                else:
                    continue
            # 抓取面积
            area = div.select('div[class="zu-info"] > p[class="details-item tag"] > b[class="strongbox"]')[
                       2].text + '平米'
            # 爬取朝向
            direct = div.select('div[class="zu-info"] > p[class="details-item bot-tag"] > span[class="cls-2"]')[0].text
            # 爬取租用类型
            hire_type = div.select('div[class="zu-info"] > p[class="details-item bot-tag"] > span[class="cls-1"]')[
                0].text
            # 抓取价格
            # print(div.select('p > strong > b[class="strongbox"]')[0].text)
            price = div.select('div[class="zu-side"] > p')[0].text

            df = df.append({
                '小区名称': name, '户型': hou_shape,
                '详细地址': address_, '面积': area,
                '价格': price, '朝向': direct,
                '租用类型': hire_type, '楼层': flo
            }, ignore_index=True)
            item_num += 1
            if item_num > max_num:
                break

        if item_num > max_num:
            print('爬取完毕')
            break
        print('当前爬取页为：', page)
        page = page + 1
        time.sleep(1)