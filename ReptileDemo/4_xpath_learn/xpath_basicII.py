# -*- coding: utf-8 -*-
# @time    : 2023/3/29 23:57
# @author  : w-xin
# @file    : xpath_basicII.py
# @software: PyCharm


from lxml import etree

if __name__ == '__main__':

    tree = etree.parse('./exampleHtml2.html')  # parse 可以直接加载 HTML 文件
    result = tree.xpath('/html')
    # print(result)  # [<Element html at 0x14ce613eb00>]

    # 找 ul 中的 li
    result = tree.xpath('/html/body/ul/li/a/text()')
    # print(result)  # [<Element a at 0x1d11f1d8140>, <Element a at 0x1d11f1d8180>, <Element a at 0x1d11f1d81c0>]  ['百度', '谷歌', '搜狗']

    # 抓取指定元素的 li; xpath 从1开始索引
    result = tree.xpath('/html/body/ul/li[1]/a/text()')
    # print(result)  # ['百度']

    # 抓取 ol 中指定 href 的内容
    result = tree.xpath('/html/body/ol/li/a[@href=\'dapao\']/text()')  # a[@href=\'dapao\'] 属性筛选
    # print(result)

    # 遍历 ul 中的 li
    ol_li = tree.xpath('/html/body/ol/li')
    for li in ol_li:
        # 从每个 li 提取信息
        # 在 li 中继续寻找信息  为相对查找
        # 根节点需要使用 ./
        li_text = li.xpath('./a/text()')
        li_href = li.xpath('./a/@href')  # 提取 a 标签里面的 href 值

    # 提取 ul 中所有的 a 标签的 href
    ul_href = tree.xpath('/html/body/ul/li/a/@href')
