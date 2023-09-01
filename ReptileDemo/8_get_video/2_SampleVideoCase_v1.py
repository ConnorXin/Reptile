# -*- coding: utf-8 -*-
# @time    : 2023/8/19 13:55
# @author  : w-xin
# @file    : 2_SampleVideoCase_v1.py
# @software: PyCharm

"""
91 看剧网站
简单版本

没有 91 看剧网站
用 http://www.fengyuanzk.com/hanguoju/caifajiadexiaoerzi/3-2.html 网址

流程
1 拿到页面源代码
2 从源代码提取 m3u8 url
3 下载 m3u8
4 读取 m3u8 文件下载视频
5 合并视频
"""
import re
import os
import time
from threading import Thread
import shutil
import requests


def run(tsList):

    shutil.rmtree(filePath + 'ts')
    os.mkdir(filePath + 'ts')

    for ts in tsList:
        # size = 0  # 初始化已下载大小
        # chunk_size = 1024  # 每次下载的数据大小
        idx = tsList.index(ts) + 1
        savePath = ts.split('/')[-1]
        if '.ts' in ts:
            start = time.time()  # 下载开始时间
            with open(f'{filePath}\\ts\\{idx}_{savePath}', mode='wb') as f:
                responseVideo = requests.get(url = m3u8_url.split('/')[0] + '//' + m3u8_url.split('/')[2] + ts,
                                             headers = header, timeout = 180)
                # content_size = int(requests.get(url=m3u8_url.split('/')[0] + '//' + m3u8_url.split('/')[2] + ts, headers=header).headers['content-length'])  # 下载文件总大小
                # for data in requests.get(url=m3u8_url.split('/')[0] + '//' + m3u8_url.split('/')[2] + ts, headers=header).iter_content(chunk_size = chunk_size):
                f.write(responseVideo.content)
                    # size += len(data)
                    # print('\r' + f'Download progress: {float(size / content_size * 100): .2f} {"▋" * int(size * 50 / content_size)}', end = '')

                responseVideo.close()
            end = time.time()  # 下载结束时间
            print(f'{idx}_{savePath} download successfully. times: {end - start: .2f}s')
            # time.sleep(1)

    print('ts fragments download completely.')

    file_tses = os.listdir(filePath + 'ts')
    file_tses.sort(key = lambda x: int(x[:x.find('_')]))
    with open(f'{filePath}fileList.txt', mode = 'w', encoding = 'utf-8') as f:
        for i in file_tses:
            f.write(f"file '{filePath}ts\\{i}'\n")
    print('file write completely.')

    # ffmpeg -f concat -safe 0 -y -i E:\fileList.txt -c copy -strict -2 F:\Video\财阀家的小儿子\episode_6.mp4


if __name__ == '__main__':

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }

    filePath = 'E:\\'  # ts所在的文件夹

    url = 'http://www.fengyuanzk.com/hanguoju/caifajiadexiaoerzi/3-9.html'
    response = requests.get(url = url, headers = header)

    # 使用 re 提取想要的 m3u8 url
    obj = re.compile(r'"url":"(?P<url>.*?)",', re.S)
    # 提取 url
    m3u8_url = obj.search(response.text).group('url')
    m3u8_url = m3u8_url.replace('\\', '')
    response.close()
    m3u8Response1 = requests.get(url = m3u8_url, headers = header)
    m3u8Content1 = m3u8Response1.text
    m3u8Final_url = m3u8_url.split('/')[0] + '//' + m3u8_url.split('/')[2] + m3u8Content1.split('\n')[2]
    m3u8Response1.close()

    # 请求第二个 m3u8 url
    m3u8Response2 = requests.get(url = m3u8Final_url, headers = header)
    m3u8Content2 = m3u8Response2.text
    m3u8Content2List = m3u8Content2.split('\n')
    tsList = list(filter(lambda x: x.find('.ts') >= 0, m3u8Content2List))
    # 循环遍历 List 下载 ts 视频片段
    idx = 1

    thread = Thread(target = run, args = (tsList,))  # 传参进行区别 且必须是元组
    thread.start()  # 多线程状态为开始工作状态，具体的执行时间由 CPU 决定

    m3u8Response2.close()

    # os.chdir(filePath)  # 设为当前的工作目录  chdir(path)函数 把path设为当前工作目录

    # for file in file_tses:
    #     os.rename(file, file.split('_')[0] + '.ts')



