# -*- coding: utf-8 -*-
# @Author  :  connor
# @Time    :  2023/8/15 13:39
# @File    :  1_WBVideo.py
# @IDE     :  PyCharm

"""
分析网站获得以下 url
https://weibo.com/tv/api/component?page=%2Ftv%2Fshow%2F1034%3A4927033256378424

防盗链
Referer: https://weibo.com/tv/show/1034:4927033256378424?mid=4927034691683732
"""
import requests


if __name__ == '__main__':

    # 访问 post 请求时注意两点
    # 1 要提交表单数据
    # 2 添加请求头参数

    oid = '1034:4940539594997790'

    videoHeader = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Referer': f'https://weibo.com/tv/show/{oid}',
        'Cookie': 'XSRF-TOKEN=X_nNOg56fmKdhIz5egZ78nAL;_s_tentry=weibo.com;Apache=5568717781886.694.1692076041734;SINAGLOBAL=5568717781886.694.1692076041734;ULV=1692076041862:1:1:1:5568717781886.694.1692076041734:;SSOLoginState=1692089835;UOR=,,login.sina.com.cn;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5yPX02GTP5aKL9fvaV9c4v5JpX5KMhUgL.Fo-4Sh2fe0zXShq2dJLoIp7LxKqL1KMLBoqLxK-LBo2LB.9ki--ciK.RiK.f;ALF=1695972594;SCF=AsVHn9TbWZcDltMpBIDGXtIxQYaourQPBkKLZWxdhKXGricaK241V-N2SKkcgI-HUw-63Y6bY-th99RroeXhgqk.;SUB=_2A25J6p-jDeRhGeNH71MU8yzIzzqIHXVqgfZrrDV8PUNbmtAGLUrykW9NSqHPYJQlKpYjr6byp6DbO6Rh5flCB9Ae;PC_TOKEN=7973be714a;WBPSESS=gN4l19SPl2zPeLrUF3_e1TEmAVnasmPFhVucUcISh2tXjTKVNC6OH5xmlFX4bC4T_P_TWkdW47grHmP94FotjfA0w13O8CY7lX41OZYDvDkd4AnccR7m7m5AenjKjQfZx33DrFW23Zif49J759Phjw==',
        'Origin': 'https://weibo.com',
        'Page-Referer': f'/tv/show/{oid}',
        'Sec-Ch-Ua': '"Not/A)Brand";v="99","GoogleChrome";v="115","Chromium";v="115"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Xsrf-Token': 'X_nNOg56fmKdhIz5egZ78nAL'
    }
    data = {
        'data': '{"Component_Play_Playinfo": {"oid": "' + oid + '"}}'
    }
    videoUrl = f'https://weibo.com/tv/api/component?page={videoHeader["Page-Referer"]}'

    videoRespond = requests.post(url=videoUrl, headers=videoHeader, data=data)
    video = videoRespond.json()['data']['Component_Play_Playinfo']['urls'][list(videoRespond.json()['data']['Component_Play_Playinfo']['urls'])[0]]
    # title = videoRespond.json()['data']['Component_Play_Playinfo']['title'].replace('\n', '').replace('| ', '').replace('|', '')

    name = 'BoomTickBoom'
    with open(f'D:/XIN/0826Concert_ChengDu/Lumen_刘雨昕/{name}.mp4', mode='wb') as f:
        f.write(requests.get(f'http:{video}').content)
    videoRespond.close()

    print(f'{name} {list(videoRespond.json()["data"]["Component_Play_Playinfo"]["urls"])[0]} DOWNLOAD SUCCESSFUL.')