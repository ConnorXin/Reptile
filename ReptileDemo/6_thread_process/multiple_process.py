# -*- coding: utf-8 -*-
# @time    : 2023/6/19 10:51
# @author  : w-xin
# @file    : multiple_process.py
# @software: PyCharm


"""
multiple process
"""
from multiprocessing import Process


# def function():
#     for i in range(1000):
#         print("子进程", i)
#
#
# if __name__ == '__main__':
#
#     p = Process(target = function)
#     p.start()
#
#     for i in range(1000):
#         print("主进程", i)



class MyProcess(Process):  # 继承 Process

    def run(self):
        for i in range(1000):
            print('子进程', i)


if __name__ == '__main__':

    p = MyProcess()
    p.start()

    for i in range(1000):
        print('主进程', i)