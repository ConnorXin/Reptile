#全局取消证书验证
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}

import requests
import bs4
import pandas as pd
import time


df = pd.DataFrame(columns = ['小区名称', '户型', '租用类型', '详细地址', '面积', '朝向', '价格', '楼层'])
# 爬取前10页数据
page = 1
item_num, max_num = 1, 3000  # 爬取2000条数据
while True:
    # 获取其中一页的源代码
    url = 'https://sz.lianjia.com/zufang/pg{}/#contentList'.format(page)
    response = requests.get(url, headers = header)
    if response.status_code != 200:
        print('终止页为', page)
        break
    response.encoding = 'utf-8'
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    div_li = soup.select('div[class="content__list--item--main"]')

    for div in div_li:
        # 爬取价格
        price = div.select('span[class="content__list--item-price"]')[0].text
        # 爬取楼层
        flo = div.select('p[class="content__list--item--des"] > span[class="hide"]')[0].text
        # 爬取租用类型
        hire_type = div.select('p[class="content__list--item--title"]')[0].text[0: 2]
        # 爬取小区名称
        txt_1 = div.select('p[class="content__list--item--title"]')[0].text
        txt_1 = txt_1.replace(' ', '')
        txt_1 = txt_1.replace('\n', '')
        T_index1 = txt_1.find('·')
        T_index2 = txt_1.find('室')
        name = txt_1[T_index1 + 1: T_index2 - 1]
        # 爬取户型
        txt_2 = div.select('p[class="content__list--item--des"]')
        for p in txt_2:
            item = p.text
            item = item.replace(' ', '')
            item = item.replace('\n', '')
            item = item.replace('精选/', '')
            item = item.split('/')
            # 爬取含有 '*室*厅*卫' 的数据
            hou_shape = item[3]
            # 爬取详细地址
            address = item[0]
            # 爬取面积
            area = item[1]
            # 爬取楼房方向
            direct = item[2]
    # print(price)
    df = df.append({
        '小区名称': name, '户型': hou_shape,
        '租用类型': hire_type, '详细地址': address,
        '面积': area, '朝向': direct,
        '价格': price, '楼层': flo
    }, ignore_index=True)

    if item_num > max_num:
        print('爬取完毕')
        break
    print('当前爬取页为：', page)
    page = page + 1
    time.sleep(1)


print(df.head())

df.to_excel('深圳租房数据_.xlsx',header=True,index=False)