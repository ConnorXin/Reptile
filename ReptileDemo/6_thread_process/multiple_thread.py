# -*- coding: utf-8 -*-
# @time    : 2023/6/19 10:36
# @author  : w-xin
# @file    : multiple_thread.py
# @software: PyCharm


"""
python Thread
"""
from threading import Thread

def func(name):
    '''
    example code
    :param name: 区别名称
    :return:
    '''

    for i in range(1000):
        print(name, i)


if __name__ == '__main__':

    # 创建多个多线程
    t1 = Thread(target = func, args = ('xin',))  # 传参进行区别 且必须是元组
    t1.start()  # 多线程状态为开始工作状态，具体的执行时间由 CPU 决定

    t2 = Thread(target = func, args = ('um',))
    t2.start()


'''
第二种写法
'''
# class MyThread(Thread):  # 继承 Thread
#
#     def run(self):
#         for i in range(1000):
#             print('子线程', i)
#
#
# if __name__ == '__main__':
#
#     t = MyThread()
#     t.start()
#
#     for i in range(1000):
#         print('主线程', i)