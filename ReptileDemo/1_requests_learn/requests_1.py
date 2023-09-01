# -*- coding: utf-8 -*-
'''
example 3
'''

import requests

if __name__ == '__main__':
    '''
    https://movie.douban.com/typerank?type_name=%E5%8A%A8%E4%BD%9C&type=5&interval_id=100:90&action=
    该网址是属于第二次请求服务器才有数据
    因此在网页源代码中并没有数据
    抓包工具中有 XHR
    第二次请求一般是 XHR

    从 XHR 中找到想要的数据的 url 即网页中的影片信息

    url: https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20
    # 以上 url 中 ? 前面的是 url; ? 后面的是参数
    在抓包工具中的 Payload 中有参数
    '''

    url = 'https://movie.douban.com/j/chart/top_list'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    # 重新封装参数
    params = {
        'type': '5',
        'interval_id': '100:90',
        'action': '',
        'start': 0,
        'limit': 20
    }

    # 发送 get 请求
    resp = requests.get(url=url, params=params, headers=headers)

    print(resp.request.url)  # 查看重新封装后的 url 结果
    print(resp.text)  # 发现什么都没输出 什么东西都没有; 加入 User_Agent 之后能够成功拿到数据
    print(resp.json())  # 转换成 json 可读性较强

    resp.close()  # 最后一定要关掉 resp