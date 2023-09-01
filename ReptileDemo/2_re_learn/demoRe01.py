# -*- coding: utf-8 -*-
import re

if __name__ == '__main__':

    '''
    findall: 匹配字符串中所有符合正则的内容
    但是使用不多 效率并不高
    '''
    li = re.findall(r'\d+', '我的电话是10086 / 10000')  # 前面加 r 之后  '\d+' 下面就没有波浪线了
    print(li)

    print('-' * 100)
    '''
    finditer: 匹配字符串中所有的内容 返回的是迭代器
    '''
    it = re.finditer(r'\d+', '我的电话是10086 / 10000')
    print(it)  # <callable_iterator object at 0x000001634023D910>
    # 从迭代器中拿东西
    for i in it:
        print(i)  # <re.Match object; span=(5, 10), match='10086'>
        print(i.group())  # 通过 group() 拿到我们想要的内容

    print('-' * 100)
    '''
    seach 返回的结果是 match 对象  需要使用 group()
    但是只能拿到第一个匹配的数据
    找到一个结果就返回
    '''
    s = re.search(r'\d+', '我的电话是10086 / 10000')
    print(s)  # <re.Match object; span=(5, 10), match='10086'>
    print(s.group())  # 10086

    print('-' * 100)
    '''
    match 从头开始匹配 开头不匹配就报错
    '''
    # s = re.match(r'\d+', '我的电话是10086 / 10000')
    # print(s.group())  # AttributeError: 'NoneType' object has no attribute 'group'; 出现此错误说明 .group 前面是空
    s = re.match(r'\d+', '10086 / 10000')
    print(s.group())  # 10086
    # s = re.match(r'\d+', 'co10086 / 10000')
    # print(s.group())  # 同样出现上面错误

    print('-' * 100)
    '''
    预加载正则表达式
    '''
    obj = re.compile(r'\d+')
    ret = obj.finditer('我的电话是10086 / 10000')
    print(ret)  # <callable_iterator object at 0x000001634023D6A0>

    print('-' * 100)
    '''
    一段 html
    <div class='xin'><span id='1'>刘雨昕</span></div>
    <div class='jay'><span id='2'>周杰伦</span></div>
    <div class='jolin'><span id='3'>郭麒麟</span></div>
    <div class='sylar'><span id='4'>范思哲</span></div>
    <div class='tory'><span id='5'>胡歌</span></div>

    (?P<group name>.*?): 在 .*? 的匹配内容前面加上 ?P<nama> 同时外面加上小括号加组；group name 表示给组起一个名字
    其他我们想要的数据同理
    '''
    htmlC = '''
    <div class='xin'><span id='1'>刘雨昕</span></div>
    <div class='jay'><span id='2'>周杰伦</span></div>
    <div class='jolin'><span id='3'>郭麒麟</span></div>
    <div class='sylar'><span id='4'>范思哲</span></div>
    <div class='tory'><span id='5'>胡歌</span></div>
    '''
    obj = re.compile(r'div class=\'.*?\'><span id=\'.*?\'>(?P<name>.*?)</span></div>', re.S)  # re.S: 让.能够匹配换行符
    result = obj.finditer(htmlC)
    for it in result:
        # print(it.group())  # 不符合我们想要的数据
        print(it.group('name'))  # 我们想要的数据