# -*- coding: utf-8 -*-
# @time    : 2023/6/19 16:52
# @author  : w-xin
# @file    : coroutine_1.py
# @software: PyCharm

"""
协程入门

input() 程序也是处于阻塞状态
requests.get(bilibili) 在网络请求返回数据之前 程序也是处于阻塞状态的
一般情况下 当程序处于 IO 操作的时候 线程都会处于阻塞状态

协程  当程序遇见了 IO 操作时 可以选择性的切换到其他任务上
在微观上是一个任务一个任务进行切换 切换条件一般是 IO 操作
在宏观上 我们能看到的其实是多个任务一起执行
多任务异步操作 都是在单线程的条件下
"""
import time


def func():
    '''
    example
    :return:
    '''
    print('我爱黎明')
    time.sleep(3)  # 让当前的线程处于阻塞状态 CPU 是不为我工作的
    # 在单线程里面出现该语句时效率是很低的 因为在这三秒钟什么都没干
    print('我真的爱黎明')


if __name__ == '__main__':

    func()