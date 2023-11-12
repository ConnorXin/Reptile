# -*- coding: utf-8 -*-
# @time    : 2023/11/11 15:50
# @file    : 3_no_title_browser.py
# @software: PyCharm

"""
无头浏览器
浏览器只需要在后头默默运行 只需要产出数据
"""
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':

    options = Options()
    options.add_experimental_option('detach', True)
    # 无头浏览器设置
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    web = Chrome(options=options)
    web.get('https://www.dianping.com/')
