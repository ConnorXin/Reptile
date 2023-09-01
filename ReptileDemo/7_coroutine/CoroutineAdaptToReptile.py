# -*- coding: utf-8 -*-
# @time    : 2023/6/19 23:17
# @author  : w-xin
# @file    : CoroutineAdaptToReptile.py
# @software: PyCharm

"""
coroutine adapt to reptile
use aiohttp module
"""
import asyncio
import aiohttp


async def aiodownload(url):
    '''
    发送请求 对 url 地址内容进行获取下载
    保存到文件
    发送请求的 Requests 需要替换成 aiohttp 中的代码进行协程操作
    :param url: 链接地址
    :return:
    '''
    file_name = url.rsplit('/', 1)[1]  # 右边切1次取第1个
    async with aiohttp.ClientSession() as session:  # aiohttp.ClientSession 相当于 requests
        # 使用 with 可以在 with 执行完成之后自动关闭 与文件操作相同
        async with session.get(url) as resp:  # 对 url 发出请求
            # resp.content.read()  # == resp.content()  读取文本的话就是 resp.text(); 原来是 resp.text
            with open(f'umIMG/{file_name}', mode='wb') as f:  # 文件读写也是 IO 操作 可以进行异步 另一个模块 aiofiles 进行异步
                f.write(await resp.content.read())  # 异步操作需要加 await

    print(file_name, 'complete!')


async def main():
    '''
    主函数中对多个 url 进行循环下载
    :return:
    '''
    tasks = [asyncio.create_task(aiodownload(url)) for url in urls]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    urls = [
        'http://kr.shanghai-jiuxin.com/file/bizhi/20220929/ug153nfffzy.jpg',
        'http://kr.shanghai-jiuxin.com/file/bizhi/20220929/kqc3vgnbnct.jpg',
        'http://kr.shanghai-jiuxin.com/file/bizhi/20220929/j3kpwqx3ply.jpg'
    ]

    '''
    asyncio+aiohttp 出现 Exception ignored：RuntimeError('Event loop is closed'):
    像 aiohttp 这类第三方协程库都是依赖于标准库 asyncio 的，而 asyncio 对 Windows 的支持本来就不好。
    Python3.8 后默认 Windows 系统上的事件循环采用 ProactorEventLoop （仅用于 Windows ）这篇文档描述了
    其在 Windows 下的缺陷：https://docs.python.org/zh-cn/3/library/asyncio-platforms.html#windows 
    引发异常的函数是 _ProactorBasePipeTransport.__del__ ，所以 aiohttp 铁定使用了 _ProactorBasePipeTransport，
    并且在程序退出释放内存时自动调用了其__del__ 方法

    解决方法:
    1 不要使用 run 函数
    既然 _ProactorBasePipeTransport 会在程序结束后自动关闭事件循环，那就不要用 run 函数了，用官网的例子，使用 loop 
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

    2 替换事件循环
    在调用 run 函数前，替换默认的 ProactorEventLoop 为 SelectorEventLoop
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    但是 SelectorEventLoop 是有一些缺点的，比如不支持子进程等
    '''
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

