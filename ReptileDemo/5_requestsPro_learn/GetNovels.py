# -*- coding: utf-8 -*-
# @time    : 2023/4/3 23:10
# @author  : w-xin
# @file    : GetNovels.py
# @software: PyCharm

"""
登录 -> 得到 cookie
带着 cookie 去请求到书架 url -> 书架上的内容
必须把以上两个操作连起来

我们可以使用 session 进行请求  -> session 可以认为是一连串的请求；在这个过程中的 cookie 不会丢失
"""
import requests

if __name__ == '__main__':
    # 准备 session
    session = requests.session()

    # 登录
    url = 'https://passport.17k.com/ck/user/login'
    data = {
        'loginName': '13823273489',
        'password': '!@#$1234qwer'
    }
    respond = session.post(url = url, data = data)
    # print(respond.text)
    # print(respond.cookies)  # 查看 cookie

    # 抓取书架的数据
    # 找到隐藏起来的书架 url 数据地址
    book_url = 'https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919'
    book_resp = session.get(url = book_url)
    print(book_resp.json())

    # 不使用 session 使用 requsets 也行 但是麻烦
    # book_resp = requests.get(url = book_url, headers = {
    #     'Cookie': 'GUID=038a8c04-dd9c-407a-a910-77af03873ef3; Hm_lvt_9793f42b498361373512340937deb2a0=1680535053,1680682714; c_channel=0; c_csc=0; __bid_n=187508248aa907f7624207; FPTOKEN=ymAwckJoUxYtm1nG+XpXyFKASi8YRVNjT3DoCVQxSQqXfbqfxxWxaGgC7h3WwoNwceUqpHZJqy3lFSafkMJZopJu+wQOTn9eFDOp29fuao2oQSXkhIQwkLkuPTzUnrcnCV5FDCxRlA7HKJEix+pmT0v0z0GpzTv0mBQiJNVSsjEk2vbl1Diuvaoi1wgmbe9dkAqOoInGIYVKeLwbG8Cyr3KO+pnbhYpMMzbBBaHqv7GDBHe0YnkDTdZFt+FV3pKp/Wi7tpCBC5ScXSXqBz4ar86ANsWkZ7DXFln6ivDQiOJUXfcd/UxiJvBQL5rJ8DZxlI4aU72Jilv0QpVryY0T5s7oQsrCOYWIsnV3vJ+JTE7HDnNc+T72KaBbeYMI2GWbEj4oEpvmdDppPKm2z5UvWw==|RonY/4VooJvfVgim2uRQ3tEY2w+r2ogRfBGZQbYX7TA=|10|b1131f64752b7cd681f340bf58390276; accessToken=avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F08%252F28%252F54%252F100135428.jpg-88x88%253Fv%253D1680683866000%26id%3D100135428%26nickname%3D%25E4%25B9%25A6%25E5%258F%258B0S9f98xF6%26e%3D1696236097%26s%3D83050cf413460f93; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22100135428%22%2C%22%24device_id%22%3A%2218747b1e20e669-01f03861f8b97d-26031851-921600-18747b1e20f107e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fgraph.qq.com%2F%22%2C%22%24latest_referrer_host%22%3A%22graph.qq.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%2C%22first_id%22%3A%22038a8c04-dd9c-407a-a910-77af03873ef3%22%7D; Hm_lpvt_9793f42b498361373512340937deb2a0=1680686033'
    # })
    # print(book_resp.text)


    session.close()
    respond.close()
    book_resp.close()