# -*- coding: utf-8 -*-
# @time    : 2023/11/11 11:12
# @file    : 2_selenium_windows_switch.py
# @software: PyCharm

"""
selenium 窗口切换
"""
import time

from selenium.webdriver import Chrome, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


if __name__ == '__main__':

    options = Options()
    options.add_experimental_option('detach', True)

    web = Chrome(options=options)

    web.get('http://lagou.com')
    web.find_element(by=By.XPATH, value='//*[@id="cboxClose"]').click()
    time.sleep(1)
    web.find_element(by=By.XPATH, value='//*[@id="search_input"]').send_keys('python', Keys.ENTER)
    time.sleep(3)
    element = web.find_element(by=By.XPATH, value='//*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/a/h3')
    web.execute_script("arguments[0].click();", element)
    time.sleep(1)
    # 视觉上是已经切换到新窗口了 但是在 selenium 中其实并没有 所以需要进行切换窗口
    # window_handles 取到 -1 最后一个就是切换到最后一个标签页
    web.switch_to.window(web.window_handles[-1])
    # 拿到岗位描述的内容
    job_describe = web.find_element(by=By.XPATH, value='//*[@id="job_detail"]/dd[2]/div').text
    print(job_describe)
    # 完成对页面的提取可以关闭并回到前一个标签页
    web.close()
    web.switch_to.window(web.window_handles[0])
    # 还能拿到页面内容说明切换过来了
    print(element.text)

