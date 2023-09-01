#全局取消证书验证
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 模拟浏览器头部
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
}

import requests
import bs4
import pandas as pd
import time


df = pd.DataFrame(columns = ['小区名称', '户型', '详细地址', '面积', '价格', '楼层', '朝向', '租用类型'])

page = 1
item_num, max_num = 1, 3000  # 爬取3000条数据
while True:
    # 获取其中一页的源代码
    url = 'https://sz.zu.anjuke.com/fangyuan/p{}/'.format(page)
    response = requests.get(url, headers = header)
    if response.status_code != 200:
        print('终止页为', page)
        break
    response.encoding = 'utf-8'
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    # div_li_1 = soup.select('div[class="zu-info"]')
    # div_li_2 = soup.select('div[class="zu-side"]')
    div_li = soup.select('div[class="zu-itemmod"]')

    for div in div_li:
        # 爬取楼层
        flo = div.select('div[class="zu-info"] > p[class="details-item tag"]')[0].text
        flo = flo.split('|')[2]
        flo_ind = flo.find(')')
        flo = flo[: flo_ind+1]
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
                address_ = address_[i: ]
                address_ = address_.strip()
            else:
                continue
        # 抓取面积
        area = div.select('div[class="zu-info"] > p[class="details-item tag"] > b[class="strongbox"]')[2].text + '平米'
        # 爬取朝向
        direct = div.select('div[class="zu-info"] > p[class="details-item bot-tag"] > span[class="cls-2"]')[0].text
        # 爬取租用类型
        hire_type = div.select('div[class="zu-info"] > p[class="details-item bot-tag"] > span[class="cls-1"]')[0].text
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


df.to_excel('Shenzhen_hirehouse_data.xlsx', header = True, index = False)


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings
import jieba
from wordcloud import WordCloud

warnings.filterwarnings('ignore')

# show chinese
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_excel('Shenzhen_hirehouse_data.xlsx')

# data presolve

# nan handle
df.dropna('index', how = 'any', inplace = True)
# check repetitive data
df.duplicated()
# delete repetitive data
df.drop_duplicates(inplace = True)

# data conversion
area_val = df['面积'].values
price_val = df['价格'].values
area = np.array([])
price = np.array([])
for i in area_val:
    area = np.append(area, np.array(i[: -2]))  # drop '平米'
for j in price_val:
    price = np.append(price, np.array(j[: -3]))  # drop '元/月'
area = area.astype(np.float64)
price = price.astype(np.float64)
df.loc[:, '面积'] = area
df.loc[:, '价格'] = price

# add column '区域'
zone_val = df['详细地址'].values
zone = np.array([])
for m in zone_val:
    zone = np.append(zone, np.array(m[: 2]))
df.insert(2, '区域', zone)
# print(df)


# zone house analysis
def zone_amount(d):
    zone_count = d.groupby('区域').count()
    zonecount_val = zone_count['小区名称'].values
    zone_df = pd.DataFrame(zonecount_val, index = zone_count.index, columns = ['房源数目'])

    # zone house visualization
    fig_1, ax = plt.subplots(2, 1, sharex = True, figsize=(16, 9), dpi=100)
    plt.tight_layout(pad = 2, h_pad = -9)

    # first fig
    ax_1 =ax[0]
    x_1 = range(len(zonecount_val))
    y_1 = zonecount_val

    bar_width = 0.6
    ax_1.bar(x_1, y_1, width = bar_width, color ='#630700')

    ax_1.set_yticks(range(0, 450, 30))
    ax_1.set_yticklabels([i for i in range(450)[::30]], fontsize = 12)
    ax_1.set_ylabel('房源数目', fontsize = 10)
    ax_1.spines['right'].set_color('none')  # hide Axial ridge
    ax_1.spines['top'].set_color('none')
    ax_1.xaxis.set_ticks_position('none')
    # ax_1.grid(alpha = 0.3, axis = 'y', color = 'b', lw = 0.25)
    for i, j in zip(x_1, y_1):
        text = ax_1.text(i, j + 6, j, ha = 'center', color = '#630700', fontsize = 14)

    # second fig
    y_2 = zone_df.values.reshape(1, 11)

    cmap = mpl.cm.Reds
    norm = mpl.colors.Normalize(vmin = 0, vmax = 500)
    ax_2 =ax[1]
    ax_2.imshow(y_2, cmap = cmap)
    plt.colorbar(mpl.cm.ScalarMappable(norm = norm, cmap = cmap),
                  orientation = 'horizontal', label = 'Some Units')

    for i in range(11):
        text = ax_2.text(i, 0, zonecount_val[i], ha = 'center', va = 'center', color = 'w', fontsize = 14)
        if i == 2 or i == 3 or i == 6:
            text = ax_2.text(i, 0, zonecount_val[i], ha = 'center', va = 'center', color = 'k', fontsize = 14)
    ax_2.set_xticks(ticks = range(0, 11, 1))
    ax_2.set_xticklabels([i for i in zone_count.index], fontsize = 14)
    ax_2.set_yticks(ticks = range(1))
    ax_2.set_xlabel('深圳各区域', fontsize = 12)
    fig_1.suptitle('深圳各区域房源分布', fontsize = 20)
    ax_2.spines['right'].set_color('none')
    ax_2.spines['top'].set_color('none')

    # save fig
    plt.savefig('zone_fig.jpg')
    # plt.show()

zone_amount(df)


def zone_areaprice(d):
    d = d.drop('zone_name', axis = 1, inplace = False)
    # divide data
    longhua_df = d[d['区域'] == '龙华']
    longhua_df.drop_duplicates(subset = '面积', keep = 'first', inplace=True)
    longhua_df = longhua_df.reset_index(drop = True)
    longhua_df = longhua_df.sort_values(by = '面积', axis = 0, ascending = True)

    longgang_df = d[d['区域'] == '龙岗']
    longgang_df.drop_duplicates(subset='面积', keep='first', inplace=True)
    longgang_df = longgang_df.reset_index(drop=True)
    longgang_df = longgang_df.sort_values(by='面积', axis=0, ascending=True)

    nanshan_df = d[d['区域'] == '南山']
    nanshan_df.drop_duplicates(subset='面积', keep='first', inplace=True)
    nanshan_df = nanshan_df.reset_index(drop=True)
    nanshan_df = nanshan_df.sort_values(by='面积', axis=0, ascending=True)

    luohu_df = d[d['区域'] == '罗湖']
    luohu_df.drop_duplicates(subset='面积', keep='first', inplace=True)
    luohu_df = luohu_df.reset_index(drop=True)
    luohu_df = luohu_df.sort_values(by='面积', axis=0, ascending=True)

    baoan_df = d[d['区域'] == '宝安']
    baoan_df.drop_duplicates(subset='面积', keep='first', inplace=True)
    baoan_df = baoan_df.reset_index(drop=True)
    baoan_df = baoan_df.sort_values(by='面积', axis=0, ascending=True)

    buji_df = d[d['区域'] == '布吉']
    buji_df.drop_duplicates(subset='面积', keep='first', inplace=True)
    buji_df = buji_df.reset_index(drop=True)
    buji_df = buji_df.sort_values(by='面积', axis=0, ascending=True)

    yantian_df = d[d['区域'] == '盐田']
    yantian_df.drop_duplicates(subset='面积', keep='first', inplace=True)
    yantian_df = yantian_df.reset_index(drop=True)
    yantian_df = yantian_df.sort_values(by='面积', axis=0, ascending=True)

    futian_df = d[d['区域'] == '福田']
    futian_df.drop_duplicates(subset='面积', keep='first', inplace=True)
    futian_df = futian_df.reset_index(drop=True)
    futian_df = futian_df.sort_values(by='面积', axis=0, ascending=True)

    guangming_df = d[d['区域'] == '光明']
    guangming_df.drop_duplicates(subset='面积', keep='first', inplace=True)
    guangming_df = guangming_df.reset_index(drop=True)
    guangming_df = guangming_df.sort_values(by='面积', axis=0, ascending=True)

    pingshan_df = d[d['区域'] == '坪山']
    pingshan_df.drop_duplicates(subset='面积', keep='first', inplace=True)
    pingshan_df = pingshan_df.reset_index(drop=True)
    pingshan_df = pingshan_df.sort_values(by='面积', axis=0, ascending=True)

    dapeng_df = d[d['区域'] == '大鹏']
    dapeng_df.drop_duplicates(subset='面积', keep='first', inplace=True)
    dapeng_df = dapeng_df.reset_index(drop=True)
    dapeng_df = dapeng_df.sort_values(by='面积', axis=0, ascending=True)
    # compute price/area
    # longhua
    # print(longhua_df)
    longhua_perarr = np.array([])
    for i in range(len(longhua_df['小区名称'])):
        perarr = longhua_df.loc[i, ['价格']].values / longhua_df.loc[i, ['面积']].values
        longhua_perarr = np.append(longhua_perarr, np.array(perarr))
    longhua_df['per-area'] = longhua_perarr
    # longgang
    longgang_perarr = np.array([])
    for i in range(len(longgang_df['小区名称'])):
        perarr = longgang_df.loc[i, ['价格']].values / longgang_df.loc[i, ['面积']].values
        longgang_perarr = np.append(longgang_perarr, np.array(perarr))
    longgang_df['per-area'] = longgang_perarr
    # nanshan
    nanshan_perarr = np.array([])
    for i in range(len(nanshan_df['小区名称'])):
        perarr = nanshan_df.loc[i, ['价格']].values / nanshan_df.loc[i, ['面积']].values
        nanshan_perarr = np.append(nanshan_perarr, np.array(perarr))
    nanshan_df['per-area'] = nanshan_perarr
    # luohu
    luohu_perarr = np.array([])
    for i in range(len(luohu_df['小区名称'])):
        perarr = luohu_df.loc[i, ['价格']].values / luohu_df.loc[i, ['面积']].values
        luohu_perarr = np.append(luohu_perarr, np.array(perarr))
    luohu_df['per-area'] = luohu_perarr
    # baoan
    baoan_perarr = np.array([])
    for i in range(len(baoan_df['小区名称'])):
        perarr = baoan_df.loc[i, ['价格']].values / baoan_df.loc[i, ['面积']].values
        baoan_perarr = np.append(baoan_perarr, np.array(perarr))
    baoan_df['per-area'] = baoan_perarr
    # buji
    buji_perarr = np.array([])
    for i in range(len(buji_df['小区名称'])):
        perarr = buji_df.loc[i, ['价格']].values / buji_df.loc[i, ['面积']].values
        buji_perarr = np.append(buji_perarr, np.array(perarr))
    buji_df['per-area'] = buji_perarr
    # yantian
    yantian_perarr = np.array([])
    for i in range(len(yantian_df['小区名称'])):
        perarr = yantian_df.loc[i, ['价格']].values / yantian_df.loc[i, ['面积']].values
        yantian_perarr = np.append(yantian_perarr, np.array(perarr))
    yantian_df['per-area'] = yantian_perarr
    # futian
    futian_perarr = np.array([])
    for i in range(len(futian_df['小区名称'])):
        perarr = futian_df.loc[i, ['价格']].values / futian_df.loc[i, ['面积']].values
        futian_perarr = np.append(futian_perarr, np.array(perarr))
    futian_df['per-area'] = futian_perarr
    # guangming
    guangming_perarr = np.array([])
    for i in range(len(guangming_df['小区名称'])):
        perarr = guangming_df.loc[i, ['价格']].values / guangming_df.loc[i, ['面积']].values
        guangming_perarr = np.append(guangming_perarr, np.array(perarr))
    guangming_df['per-area'] = guangming_perarr
    # pingshan
    pingshan_perarr = np.array([])
    for i in range(len(pingshan_df['小区名称'])):
        perarr = pingshan_df.loc[i, ['价格']].values / pingshan_df.loc[i, ['面积']].values
        pingshan_perarr = np.append(pingshan_perarr, np.array(perarr))
    pingshan_df['per-area'] = pingshan_perarr
    # dapeng
    dapeng_perarr = np.array([])
    for i in range(len(dapeng_df['小区名称'])):
        perarr = dapeng_df.loc[i, ['价格']].values / dapeng_df.loc[i, ['面积']].values
        dapeng_perarr = np.append(dapeng_perarr, np.array(perarr))
    dapeng_df['per-area'] = dapeng_perarr
    # area-price visualization
    fig = plt.figure(figsize=(16, 9), dpi=100)

    # longhua
    ax_10 = fig.add_subplot(341)
    x_9 = longhua_df['面积'].values
    y_9 = longhua_df['per-area'].values
    line_1 = ax_10.plot(x_9, y_9, color = 'brown', lw = 1.5)
    ax_10.set_ylabel('每平米均价', fontsize = 12)
    # longgang
    ax_11 = fig.add_subplot(342)
    x_10 = longgang_df['面积'].values
    y_10 = longgang_df['per-area'].values
    line_2 = ax_11.plot(x_10, y_10, color='dimgray', lw=1.5)
    # nanshan
    ax_12 = fig.add_subplot(343)
    x_11 = nanshan_df['面积'].values
    y_11 = nanshan_df['per-area'].values
    line_3 = ax_12.plot(x_11, y_11, color='darkorange', lw=1.5)
    # luohu
    ax_13 = fig.add_subplot(344)
    x_12 = luohu_df['面积'].values
    y_12 = luohu_df['per-area'].values
    line_4 = ax_13.plot(x_12, y_12, color='lime', lw=1.5)
    # baoan
    ax_14 = fig.add_subplot(345)
    x_13 = baoan_df['面积'].values
    y_13 = baoan_df['per-area'].values
    line_5 = ax_14.plot(x_13, y_13, color='m', lw=1.5)
    # buji
    ax_15 = fig.add_subplot(346)
    x_14 = buji_df['面积'].values
    y_14 = buji_df['per-area'].values
    line_6 = ax_15.plot(x_14, y_14, color='cornflowerblue', lw=1.5)
    # yantian
    ax_16 = fig.add_subplot(347)
    x_15 = yantian_df['面积'].values
    y_15 = yantian_df['per-area'].values
    line_7 = ax_16.plot(x_15, y_15, color='aqua', lw=1.5)
    # futian
    ax_17 = fig.add_subplot(348)
    x_16 = futian_df['面积'].values
    y_16 = futian_df['per-area'].values
    line_8 = ax_17.plot(x_16, y_16, color='midnightblue', lw=1.5)
    # guangming
    ax_18 = fig.add_subplot(349)
    x_17 = guangming_df['面积'].values
    y_17 = guangming_df['per-area'].values
    line_9 = ax_18.plot(x_17, y_17, color='darkgreen', lw=1.5)
    # pingshan
    ax_19 = fig.add_subplot(3, 4, 10)
    x_18 = pingshan_df['面积'].values
    y_18 = pingshan_df['per-area'].values
    line_10 = ax_19.plot(x_18, y_18, color='mediumslateblue', lw=1.5)
    # dapeng
    ax_20 = fig.add_subplot(3, 4, 11)
    x_19 = dapeng_df['面积'].values
    y_19 = dapeng_df['per-area'].values
    line_11 = ax_20.plot(x_19, y_19, color='chocolate', lw=1.5)
    ax_20.set_xlabel('房源面积', fontsize = 12)

    fig.suptitle('各区域房源面积对每平米均价的影响曲线', fontsize = 20)
    # add legend
    ax_10.legend(line_1, ('龙华',), prop={'family': 'SimHei', 'size': 10}, loc='upper right')
    ax_11.legend(line_2, ('龙岗',), prop={'family': 'SimHei', 'size': 10}, loc='upper right')
    ax_12.legend(line_3, ('南山',), prop={'family': 'SimHei', 'size': 10}, loc='upper right')
    ax_13.legend(line_4, ('罗湖',), prop={'family': 'SimHei', 'size': 10}, loc='upper right')
    ax_14.legend(line_5, ('宝安',), prop={'family': 'SimHei', 'size': 10}, loc='upper right')
    ax_15.legend(line_6, ('布吉',), prop={'family': 'SimHei', 'size': 10}, loc='upper right')
    ax_16.legend(line_7, ('盐田',), prop={'family': 'SimHei', 'size': 10}, loc='upper right')
    ax_17.legend(line_8, ('福田',), prop={'family': 'SimHei', 'size': 10}, loc='upper right')
    ax_18.legend(line_9, ('光明',), prop={'family': 'SimHei', 'size': 10}, loc='upper right')
    ax_19.legend(line_10, ('坪山',), prop={'family': 'SimHei', 'size': 10}, loc='upper right')
    ax_20.legend(line_11, ('大鹏',), prop={'family': 'SimHei', 'size': 10}, loc='upper right')

    # save fig
    plt.savefig('areaprice_fig.jpg')

zone_areaprice(df)


def address_cloud(d):
    d = d.drop('zone_name', axis=1, inplace=False)
    # add address
    add_val = d['详细地址'].values
    address = np.array([])
    for n in add_val:
        address = np.append(address, np.array(n[3:]))
    d.insert(3, '地址', address)

    # longhua
    longhua_df = d[d['区域'] == '龙华']
    longhua_s = longhua_df['地址'].values
    longhua_ToStr = ','.join(map(str, longhua_s))
    longhua_txt = longhua_ToStr
    words_1 = jieba.lcut(longhua_txt)  # divide word
    newtxt_1 = ''.join(words_1)  # space join
    # wordcloud_1 = WordCloud(font_path='msyh.ttc', background_color='white',
    #                       width=1000, height=900, max_words=15)
    wordcloud_1 = WordCloud(font_path = 'msyh.ttc', width = 1000, height = 900, background_color = 'white')
    wordcloud_1 = wordcloud_1.generate(newtxt_1)
    wordcloud_1.to_file('longhuacloud_fig.jpg')
    # longgang
    longgang_df = d[d['区域'] == '龙岗']
    longgang_s = longgang_df['地址'].values
    longgang_ToStr = ','.join(map(str, longgang_s))
    longgang_txt = longgang_ToStr
    words_2 = jieba.lcut(longgang_txt)  # divide word
    newtxt_2 = ''.join(words_2)  # space join
    wordcloud_2 = WordCloud(font_path='msyh.ttc', width=1000, height=900, background_color='white')
    wordcloud_2 = wordcloud_2.generate(newtxt_2)
    wordcloud_2.to_file('longgangcloud_fig.jpg')
    # nanshan
    nanshan_df = d[d['区域'] == '南山']
    nanshan_s = nanshan_df['地址'].values
    nanshan_ToStr = ','.join(map(str, nanshan_s))
    nanshan_txt = nanshan_ToStr
    words_3 = jieba.lcut(nanshan_txt)  # divide word
    newtxt_3 = ''.join(words_3)  # space join
    wordcloud_3 = WordCloud(font_path='msyh.ttc', width=1000, height=900, background_color='white')
    wordcloud_3 = wordcloud_3.generate(newtxt_3)
    wordcloud_3.to_file('nanshancloud_fig.jpg')
    # luohu
    luohu_df = d[d['区域'] == '罗湖']
    luohu_s = luohu_df['地址'].values
    luohu_ToStr = ','.join(map(str, luohu_s))
    luohu_txt = luohu_ToStr
    words_4 = jieba.lcut(luohu_txt)  # divide word
    newtxt_4 = ''.join(words_4)  # space join
    wordcloud_4 = WordCloud(font_path='msyh.ttc', width=1000, height=900, background_color='white')
    wordcloud_4 = wordcloud_4.generate(newtxt_4)
    wordcloud_4.to_file('luohucloud_fig.jpg')
    # baoan
    baoan_df = d[d['区域'] == '宝安']
    baoan_s = baoan_df['地址'].values
    baoan_ToStr = ','.join(map(str, baoan_s))
    baoan_txt = baoan_ToStr
    words_5 = jieba.lcut(baoan_txt)  # divide word
    newtxt_5 = ''.join(words_5)  # space join
    wordcloud_5 = WordCloud(font_path='msyh.ttc', width=1000, height=900, background_color='white')
    wordcloud_5 = wordcloud_5.generate(newtxt_5)
    wordcloud_5.to_file('baoancloud_fig.jpg')
    # buji
    buji_df = d[d['区域'] == '布吉']
    buji_s = buji_df['地址'].values
    buji_ToStr = ','.join(map(str, buji_s))
    buji_txt = buji_ToStr
    words_6 = jieba.lcut(buji_txt)  # divide word
    newtxt_6 = ''.join(words_6)  # space join
    wordcloud_6 = WordCloud(font_path='msyh.ttc', width=1000, height=900, background_color='white')
    wordcloud_6 = wordcloud_6.generate(newtxt_6)
    wordcloud_6.to_file('bujicloud_fig.jpg')
    # yantian
    yantian_df = d[d['区域'] == '盐田']
    yantian_s = yantian_df['地址'].values
    yantian_ToStr = ','.join(map(str, yantian_s))
    yantian_txt = yantian_ToStr
    words_7 = jieba.lcut(yantian_txt)  # divide word
    newtxt_7 = ''.join(words_7)  # space join
    wordcloud_7 = WordCloud(font_path='msyh.ttc', width=1000, height=900, background_color='white')
    wordcloud_7 = wordcloud_7.generate(newtxt_7)
    wordcloud_7.to_file('yantiancloud_fig.jpg')
    # futian
    futian_df = d[d['区域'] == '福田']
    futian_s = futian_df['地址'].values
    futian_ToStr = ','.join(map(str, futian_s))
    futian_txt = futian_ToStr
    words_8 = jieba.lcut(futian_txt)  # divide word
    newtxt_8 = ''.join(words_8)  # space join
    wordcloud_8 = WordCloud(font_path='msyh.ttc', width=1000, height=900, background_color='white')
    wordcloud_8 = wordcloud_8.generate(newtxt_8)
    wordcloud_8.to_file('futiancloud_fig.jpg')
    # guangming
    guangming_df = d[d['区域'] == '光明']
    guangming_s = guangming_df['地址'].values
    guangming_ToStr = ','.join(map(str, guangming_s))
    guangming_txt = guangming_ToStr
    words_9 = jieba.lcut(guangming_txt)  # divide word
    newtxt_9 = ''.join(words_9)  # space join
    wordcloud_9 = WordCloud(font_path='msyh.ttc', width=1000, height=900, background_color='white')
    wordcloud_9 = wordcloud_9.generate(newtxt_9)
    wordcloud_9.to_file('guangmingcloud_fig.jpg')
    # pingshan
    pingshan_df = d[d['区域'] == '坪山']
    pingshan_s = pingshan_df['地址'].values
    pingshan_ToStr = ','.join(map(str, pingshan_s))
    pingshan_txt = pingshan_ToStr
    words_10 = jieba.lcut(pingshan_txt)  # divide word
    newtxt_10 = ''.join(words_10)  # space join
    wordcloud_10 = WordCloud(font_path='msyh.ttc', width=1000, height=900, background_color='white')
    wordcloud_10 = wordcloud_10.generate(newtxt_10)
    wordcloud_10.to_file('pingshancloud_fig.jpg')
    # dapeng
    dapeng_df = d[d['区域'] == '大鹏']
    dapeng_s = dapeng_df['地址'].values
    dapeng_ToStr = ','.join(map(str, dapeng_s))
    dapeng_txt = dapeng_ToStr
    words_11 = jieba.lcut(dapeng_txt)  # divide word
    newtxt_11 = ''.join(words_11)  # space join
    wordcloud_11 = WordCloud(font_path='msyh.ttc', width=1000, height=900, background_color='white')
    wordcloud_11 = wordcloud_11.generate(newtxt_11)
    wordcloud_11.to_file('dapengcloud_fig.jpg')

address_cloud(df)