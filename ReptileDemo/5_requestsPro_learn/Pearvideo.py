# -*- coding: utf-8 -*-
# @time    : 2023/4/5 19:42
# @author  : w-xin
# @file    : Pearvideo.py
# @software: PyCharm

"""
梨视频视频爬取     https://pearvideo.com/

在开发者工具中能够找到 video 标签的视频链接
但是在网页源代码并没有 video 标签  说明此视频有可能是后期通过 js 二次加载进去的
开发者工具中的源代码与页面源代码是有偏差的
"""
import requests

if __name__ == '__main__':

    original_url = 'https://pearvideo.com/video_1693830'

    contId = original_url.split('_')[1]

    # 通过这个 url 拿到视频相关的 json
    # 把 json 里面的 srcurl 并且需要把里面的部分链接替换掉得到视频链接
    video_status = f'https://pearvideo.com/videoStatus.jsp?contId={contId}&mrd=0.7503395563056279'

    '''
    Referer: https://pearvideo.com/video_1693830
    Header 下面有个 Referer 为防盗链
    防盗链: 溯源，当前链接的上一级链接
    header 中加上防盗链就能拿到 srcurl 的 json
    '''

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        'Referer': 'https://pearvideo.com/video_1693830'
    }

    # 通过 requests 拿到 video_status 中的 json
    respond = requests.get(url = video_status, headers = header)
    srcurl = respond.json()['videoInfo']['videos']['srcUrl']
    systemTime = respond.json()['systemTime']
    # print(systemTime)

    # srcurl: https://video.pearvideo.com/mp4/adshort/20200826/1680695370568-15348904_adpkg-ad_hd.mp4
    # videourl: https://video.pearvideo.com/mp4/adshort/20200826/cont-1693830-15348904_adpkg-ad_hd.mp4
    # 对 srcurl 进行替换 拿到真实的视频链接

    video_utl = srcurl.replace(systemTime, 'cont-' + contId)
    # print(video_utl)


    # 下载视频
    with open('./pearvidel.mp4', mode = 'wb') as f:
        f.write(requests.get(video_utl).content)

    print('download over!')

    respond.close()
