# -*- coding: utf-8 -*-
# @time    : 2023/3/29 23:33
# @author  : w-xin
# @file    : xpath_basic.py
# @software: PyCharm
from lxml import etree

if __name__ == '__main__':

    xml = '''
    <book>
    <id>l</id>
    <name>野花遍地香</name>
    <price>1.23</price>
    <nick>土豆洋芋</nick>
    <author>
        <nick id="10086">刘雨昕</nick>
        <nick id="10000">胡歌</nick>
        <nick class="xin">XINLIU</nick>
        <nick class="wangyang">王阳</nick>
        <div>
            <nick>刘雨昕！1</nick>
        </div>
        <span>
            <nick>刘雨昕！2</nick>
        </span>
        
    </author>

    <partner>
        <nick id="ppc">胖胖陈</nick>
        <nick id="ppbc">胖胖不陈</nick>
    </partner>
    </book>'''


    tree = etree.XML(xml)
    result = tree.xpath('/book')  # / 表示层级关系  第一个 / 是根节点
    # print(result)  # [<Element book at 0x26e04d5ebc0>]

    result = tree.xpath('/book/name')
    # print(result)  # [<Element name at 0x255eb6a8080>]
    # 想看标签内容
    result = tree.xpath('/book/name/text()')  # text() 表示拿到标签里面的文本
    # print(result)  # ['野花遍地香']


    # 拿取 nick 标签内容
    result = tree.xpath('/book/author/nick/text()')
    # print(result)  # ['刘雨昕', '胡歌', 'XINLIU', '王阳']

    result = tree.xpath('/book/author/div/nick/text()')
    # print(result)  # ['刘雨昕！']

    # 把 author 里面的内容一次性输出
    result = tree.xpath('/book/author//nick/text()')  # // 表示把 author 这个父节点里面的所有子节点内容都拿到
    # print(result)  # ['刘雨昕', '胡歌', 'XINLIU', '王阳', '刘雨昕！']  ['刘雨昕', '胡歌', 'XINLIU', '王阳', '刘雨昕！1', '刘雨昕！2', '刘雨昕！3']

    # 修改 div 为 span
    # 需要把刘雨昕！1  刘雨昕！2 一次拿到
    result = tree.xpath('/book/author/*/nick/text()')  # * 表示任意节点
    print(result)  # ['刘雨昕！1', '刘雨昕！2']