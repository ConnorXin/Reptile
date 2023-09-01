# -*- coding: utf-8 -*-
# @time    : 2023/6/20 19:22
# @author  : w-xin
# @file    : Case_BaiDuNovel.py
# @software: PyCharm

"""
coroutine to get Baidu Novel
the first url: https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"4306063500"}   %22 就是 "  得到所有章节的内容(名称 cid)
the second url: https://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4306063500","cid":"4306063500|1569782244","need_bookinfo":1}  ==>  得到小说内容

操作流程
1 同步操作 访问 getCatalog 即 the first url  拿到所有章节的名称和 cid
2 异步操作 访问 getChapterContent 下载所有的文章内容
"""
import asyncio
import json

import aiofiles as aiofiles
import aiohttp
import requests


async def aiodownload(cid, book_id, title):
    '''
    下载小说内容
    :param cid: 章节 cid
    :param book_id: 书的 id
    :param title: 章节名
    :return:
    '''
    data = {
        "book_id": book_id,
        "cid": f"{book_id}|{cid}",
        "need_bookinfo": 1
    }
    # 需要把 data 变成 json 字符串
    data = json.dumps(data)
    url = f'https://dushu.baidu.com/api/pc/getChapterContent?data={data}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            # 读取 json 字典
            contentJson = await resp.json()
            # 从 json 中获取内容
            # data ==> novel ==> content
            content = contentJson['data']['novel']['content']
            # with open(f'XiYouJi/{title}.txt', mode = 'w', encoding = 'utf-8') as f:
            #     f.write(content)
            # 异步读写文件
            async with aiofiles.open(f'XiYouJi/{title}.txt', mode = 'w', encoding = 'utf-8') as f:
                await f.write(content)


    print(f'{title} download complete!')


async def getCatalog(url):
    '''
    获取小说名称和章节 cid
    :param url: 小说章节 url
    :return:
    '''
    resp = requests.get(url)
    # 使用 json 拿到 cid
    resp_jsonDict = resp.json()
    # data ==> novel ==> items
    tasks = []
    for item in resp_jsonDict['data']['novel']['items']:  # item 对应每个章节名称和 cid
        title = item['title']
        cid = item['cid']
        # 每一个 url 就是一个异步任务
        # 从这里开始准备异步
        tasks.append(asyncio.create_task(aiodownload(cid = cid, book_id = book_id, title = title)))

    await asyncio.wait(tasks)
    # print(resp_jsonDict)




if __name__ == '__main__':

    book_id = '4306063500'
    first_url = 'https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":' + book_id + '}'

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(getCatalog(first_url))