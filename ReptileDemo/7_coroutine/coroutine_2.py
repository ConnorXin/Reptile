# -*- coding: utf-8 -*-
# @time    : 2023/6/19 22:26
# @author  : w-xin
# @file    : coroutine_2.py
# @software: PyCharm

"""
coroutine_2
"""
import asyncio
import time


async def func():
    '''
    加一个前缀 async 变成异步执行
    变成异步协程函数 此时函数执行得到的是一个协程对象
    :return:
    '''
    print('Hello World')


# async def func1():
#     '''
#     function 1
#     :return:
#     '''
#     print('function one')
#     # time.sleep(3)
#     await asyncio.sleep(3)
#     print('function one executing...')
#
#
# async def func2():
#     '''
#     function 2
#     :return:
#     '''
#     print('function two')
#     # time.sleep(2)  # time.sleep(2) 是同步操作 出现同步操作时 异步就中断了
#     await asyncio.sleep(3)  # 异步操作代码 await 是挂起的意思
#     print('function two executing...')
#
#
# async def func3():
#     '''
#     function 3
#     :return:
#     '''
#     print('function three')
#     # time.sleep(5)
#     await asyncio.sleep(5)
#     print('function three executing...')
#
#
# if __name__ == '__main__':
#
#     f = func()
#     # 借助 asyncio 模块去运行协程函数
#     # asyncio.run(f)  # 由于是单个任务 能够运行但不见得高效
#
#     f1 = func1()
#     f2 = func2()
#     f3 = func3()
#
#     # 将任务都放进一个列表里面
#     tasks = [f1, f2, f3]  # python 3.8 以后的版本需要手动将 tasks 里面的东西包装成 Tasks 对象
#     tasks = [asyncio.create_task(f1), asyncio.create_task(f2), asuncio.create_task(f3)]
#
#     t1 = time.time()
#     # 使用协程一次性启动多个任务
#     asyncio.run(asyncio.wait(tasks))
#     t2 = time.time()
#     print(t2 - t1)

    '''
    但是以上代码一般不这么写 会导致 main 主线程任务居多
    
    可以改写成以下代码
    '''


async def func1():
    '''
    function 1
    :return:
    '''
    print('function one')
    # time.sleep(3)
    await asyncio.sleep(3)
    print('function one executing...')


async def func2():
    '''
    function 2
    :return:
    '''
    print('function two')
    # time.sleep(2)  # time.sleep(2) 是同步操作 出现同步操作时 异步就中断了
    await asyncio.sleep(3)  # 异步操作代码 await 是挂起的意思
    print('function two executing...')


async def func3():
    '''
    function 3
    :return:
    '''
    print('function three')
    # time.sleep(5)
    await asyncio.sleep(5)
    print('function three executing...')


async def main():
    '''
    在 main 主线程前写个 main 函数
    在这个函数里面希望将上方三个任务同时跑起来
    :return:
    '''
    # write method one
    # f1 = func1()
    # await f1  # await 一般放在协程对象前面
    # write methos two  recommodate
    tasks = [asyncio.create_task(func1()), asyncio.create_task(func2()), asyncio.create_task(func3())]
    await asyncio.wait(tasks)


if __name__ == '__main__':

    t1 = time.time()
    # 直接调用 main 函数
    asyncio.run(main())
    t2 = time.time()
    print(t2 - t1)

    # await f1  # await 在这里用不行 必须要有 async 前缀的函数里面
