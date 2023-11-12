# -*- coding: utf-8 -*-
# @time    : 2023/11/8 10:56
# @file    : 1_selenium_base.py
# @software: PyCharm

"""
能不能让我的程序连接到浏览器 让浏览器来完成各种复杂的操作 最终只接受结果
selenium: 自动化测试工具
可以实现打开浏览器 像人一样去操作浏览器
程序员可以从 selenium 中直接提取网页上的各种信息
环境搭建
    1 pip install selenium
    2 安装浏览器驱动
        114 以下版本驱动 https://chromedriver.storage.googleapis.com/index.html
        118 119 版本驱动 https://googlechromelabs.github.io/chrome-for-testing/
        确定当前浏览器版本下载对应版本的驱动 最新版本就下载最新的驱动即可
        将 chromedriver 放在 python 解释器所在的文件夹
"""
import time

from selenium.webdriver import Chrome, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


if __name__ == '__main__':

    # 防止浏览器窗口闪退
    options = Options()
    options.add_experimental_option('detach', True)
    # 1 创建浏览器对象
    web = Chrome(options=options)
    # 2 打开网址
    web.get('http://lagou.com')
    # print(web.title)

    # 通过 xpath 找信息
    # 点击全国
    el = web.find_element(by=By.XPATH, value='//*[@id="changeCityBox"]/p[1]/a')
    el.click()  # 需要点击
    # 点击完成后加上 sleep 防止加载过慢导致下面操作比加载更快执行
    time.sleep(1)
    # 寻找输入框 输入 python 1. 可以敲 Enter 2. 也可以点击搜索按钮
    # send_keys('')  往搜索框输入信息; Keys.ENTER: 回车搜索
    web.find_element(by=By.XPATH, value='//*[@id="search_input"]').send_keys('python', Keys.ENTER)
    time.sleep(1)
    # 查找存放数据的位置 进行数据提取
    # 找到所有 div 块
    lis_list = web.find_elements(by=By.XPATH, value='//*[@id="s_position_list"]/ul/li')
    for li in lis_list:
        job_name = li.find_element(by=By.TAG_NAME, value='h3').text
        job_addr = li.find_element(by=By.XPATH, value='./div[1]/div[1]/div[1]/a/span').text
        job_company = li.find_element(by=By.XPATH, value='./div[1]/div[2]/div[1]/a').text
        job_income = li.find_element(by=By.XPATH, value='./div[1]/div[1]/div[2]/div/span').text

        print(job_name, job_addr, job_company, job_income)
