# -*- coding: utf-8 -*-
# @time    : 2023/4/6 23:48
# @author  : w-xin
# @file    : what_thread.py
# @software: PyCharm


"""
以下程序并不是多线程的程序
是单线程程序

func 函数执行完成之后执行 func 下面的循环
"""

def func():
    '''
    示例程序
    :return:
    '''
    for i in range(1000):
        print('func', i)


if __name__ == '__main__':

    func()
    for i in range(1000):
        print('main', i)
