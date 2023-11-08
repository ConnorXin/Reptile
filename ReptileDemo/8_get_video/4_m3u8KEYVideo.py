# -*- coding: utf-8 -*-
# @time    : 2023/8/23 22:59
# @author  : w-xin
# @file    : 4_m3u8KEYVideo.py
# @software: PyCharm

"""
有加密的 m3u8
"""
import os
import re
import shutil
import time
import requests
import asyncio
import aiohttp
import aiofiles
from Crypto.Cipher import AES
from subprocess import run
from Crypto.Util.Padding import pad


async def aioTsDownload(ts, session, tsList):

    idx = tsList.index(ts)
    savePath = ts.split('/')[-1]
    try:
        async with session.get(url=ts, timeout=180) as resp:
            async with aiofiles.open(f'{filePath}\\ts\\{idx}_{savePath}', mode='wb') as f:
                start = time.time()
                await f.write(await resp.content.read())
                end = time.time()
            print(f'{idx}_{savePath} download successfully. times: {end - start: .2f}s  length: {resp.content_length}')
    except:
        print('-' * 33)
        print(f'** {idx}_{savePath} Respond Again - Download Begin **')
        i = 0
        # while i < 2:
        #     try:
        async with session.get(url=ts, timeout=180) as resp:
            async with aiofiles.open(f'{filePath}\\ts\\{idx}_{savePath}', mode='wb') as f:
                start = time.time()
                # videoByte = resp.content.read()
                # # 解密
                # videoDEC = aes.decrypt(videoByte)
                await f.write(await resp.content.read())
                end = time.time()
            print(f'** {idx}_{savePath} download successfully. times: {end - start: .2f}s  length: {await resp.content_length}**')
            #         break
            # except:
            #     i += 1
        print('#' * 33)


async def aioGetList(m3u8Content):

    shutil.rmtree(filePath + 'ts')
    os.mkdir(filePath + 'ts')

    # 避免每次任务创建 aiohttp 在这里先创建以参数传过去
    async with aiohttp.ClientSession() as session:
        tsTasks = []
        tsList = [ts for ts in m3u8Content.split('\n') if 'https' in ts]
        for ts in m3u8Content.split('\n'):
            if 'https' in ts:
                tsTask = asyncio.create_task(aioTsDownload(ts, session, tsList))
                tsTasks.append(tsTask)
        await asyncio.wait(tsTasks)


async def aioMergeVideo():

    file_tses = os.listdir(filePath + 'tsDECO')
    file_tses.sort(key=lambda x: int(x[:x.find('_')]))
    async with aiofiles.open(f'{filePath}fileList.txt', mode='w', encoding='utf-8') as f:
        for i in file_tses:
            await f.write(f"file '{filePath}tsDECO\\{i}'\n")
    print('file write completely.')


def getKey(url):

    response = requests.get(url=url, headers=header)

    return response.text.encode('utf-8')


async def aioTsDECO(key):

    shutil.rmtree(filePath + 'tsDECO')
    os.mkdir(filePath + 'tsDECO')
    aes = AES.new(key=key, IV=b'0000000000000000', mode=AES.MODE_CBC)
    dirFile = os.listdir(filePath + 'ts')
    for f in dirFile:
        async with aiofiles.open(f'{filePath}ts\\{f}', mode='rb') as f1,\
            aiofiles.open(f'{filePath}tsDECO\\{f}', mode='wb') as f2:
            length = len([i for i in await f1.read()])
            print(length)
            # videoByte = await f1.read()
            # if len(await f1.read()) % 16 != 0:
            #     print(await f1.read())
            # await f2.write(aes.decrypt(await f1.read()))
    print('-' * 33)
    print('ALL VIDEO DECODE COMPELETELY.')


if __name__ == '__main__':

    header = {
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    filePath = 'E:\\'
    for episode in range(1, 12):
        print(f'-- VIDEO {episode} BEGIN --')
        origianlUrl = f'http://www.fengyuanzk.com/guocanju/liaobuqidedxiaojie/1-{episode}.html'
        originalUrlResponse = requests.get(url=origianlUrl, headers=header)

        obj = re.compile(r'"url":"(?P<m3u8URL>.*?)",', re.S)
        m3u8URL = obj.search(originalUrlResponse.text).groups('m3u8URL')[0].replace('\\', '')
        m3u8Response = requests.get(url=m3u8URL, headers=header)
        m3u8Content = m3u8Response.text
        originalUrlResponse.close()
        m3u8Response.close()

        # 异步协程下载
        asyncio.run(aioGetList(m3u8Content))

        print('ts fragments download completely.')

        # 解密
        keyURI = [uri.split('URI="')[1].split('IV=')[0].replace('",', '') for uri in m3u8Content.split('\n') if 'URI' in uri][0]
        iv = [uri.split('URI="')[1].split('IV=')[1] for uri in m3u8Content.split('\n') if 'URI' in uri][0]
        keyURL = m3u8URL.split('index.m3u8')[0] + keyURI
        key = getKey(keyURL)  # 拿到密钥
        asyncio.run(aioTsDECO(key))

        asyncio.run(aioMergeVideo())

        cmd_str = f'ffmpeg -f concat -safe 0 -y -i E:\\fileList.txt -c copy -strict -2 F:\\Video\\Good_Thing_Double\\episode_{episode}.mp4'
        run(cmd_str, shell=True)
        print('-' * 33)
        # print(f'video {episode} merge completely.')
        print(f'video merge completely.')
        print('=' * 33)
        break


