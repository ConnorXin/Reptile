# -*- coding: utf-8 -*-
# @time    : 2023/6/19 23:00
# @author  : w-xin
# @file    : reptile_coroutine.py
# @software: PyCharm

"""
coroutine for reptile
could serve as moudle to use
"""
import asyncio


async def download(url):
    '''
    download module
    :param url: website url
    :return:
    '''
    print('download start')
    await asyncio.sleep(2)  # 模拟网络请求  requests.get()
    print('download complete')


async def main():
    '''
    main function
    :return:
    '''
    urls = ['url1', 'url2', 'url3']

    tasks = []
    for url in urls:
        d = asyncio.create_task(download(url))
        tasks.append(d)

    # for 循环也可以这样写
    # tasks = [asyncio.create_task(download(url)) for url in urls]

    await asyncio.wait(tasks)

if __name__ == '__main__':

        asyncio.run(main())
