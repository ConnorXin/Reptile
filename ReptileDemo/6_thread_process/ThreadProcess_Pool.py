# -*- coding: utf-8 -*-
# @time    : 2023/6/19 13:04
# @author  : w-xin
# @file    : ThreadProcess_Pool.py
# @software: PyCharm

"""
Thread & Process Pool
"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def fn(name):


    for i in range(1000):
        print(name, i)


if __name__ == '__main__':

    # 创建线程池
    with ThreadPoolExecutor(50) as t:  # 创建50个线程的线程池
        for i in range(100):  # 100个任务交给线程池
            t.submit(fn, name = f'线程{i}')  # 向线程池提交任务

    # 等待线程池中的任务全部执行完毕，才继续执行
    print('333')

    # 改成进程即把名称改了