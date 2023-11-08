# -*- coding: utf-8 -*-
# @time    : 2023/9/2 15:37
# @author  : w-xin
# @file    : 2_WB_Video_V2.py
# @software: PyCharm

"""
"""
import requests

if __name__ == '__main__':

    while True:
        oid = input('Input video oid:')

        videoHeader = {
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Cookie': 'SINAGLOBAL=6564952634909.906.1680697786553;XSRF-TOKEN=qxOdfo9CeVsl0GoyL9Q3k_Qn;SSOLoginState=1693499156;_s_tentry=-;Apache=9037331429927.24.1693627327381;ULV=1693627327524:4:1:1:9037331429927.24.1693627327381:1684675371845;UOR=,,login.sina.com.cn;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5yPX02GTP5aKL9fvaV9c4v5JpX5KMhUgL.Fo-4Sh2fe0zXShq2dJLoIp7LxKqL1KMLBoqLxK-LBo2LB.9ki--ciK.RiK.f;ALF=1701828084;SCF=Av3iORL8Riuy7ud6FHByhTxZLppQDaFKxx6J5M4vO6QNmMlW-PFnSjUrDB7PkUQq7QrDHbsg2aD8BO9TNmOO2wk.;SUB=_2A25ITDilDeRhGeNH71MU8yzIzzqIHXVrIDRtrDV8PUNbmtAGLWetkW9NSqHPYDWZosdUc8XC4sPc_HdifxEueMwn;WBPSESS=gN4l19SPl2zPeLrUF3_e1RiVlFcP6atP92aPv9_1_QZWSNZc6UMtaJ2uCQR6L-gKOkfMeqPXoG-yV8_mQzkERmuLrlLtOxBsRE8gYs3kx6FMUSGN-PXD8X9RvVw6LAG5',
            'Referer': 'https://weibo.com/',
            'Origin': 'https://weibo.com',
            'Page-Referer': f'/tv/show/{oid}',
            'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Xsrf-Token': 'qxOdfo9CeVsl0GoyL9Q3k_Qn',
            'Ssl_node': 'mweibo-sslv6-003.yf.intra.weibo.cn'
        }
        data = {
            'data': '{"Component_Play_Playinfo": {"oid": "' + oid + '"}}'
        }

        videoUrl = f'https://weibo.com/tv/api/component?page={videoHeader["Page-Referer"]}'

        videoRespond = requests.post(url=videoUrl, headers=videoHeader, data=data)
        video = videoRespond.json()['data']['Component_Play_Playinfo']['urls'][list(videoRespond.json()['data']['Component_Play_Playinfo']['urls'])[0]]
        # title = videoRespond.json()['data']['Component_Play_Playinfo']['title'].replace('\n', '').replace('| ', '').replace('|', '')

        save_path = input('Input save path:')
        title = input('Input filename:')
        name = title
        with open(f'{save_path}\\{name}.mp4', mode='wb') as f:
            f.write(requests.get(f'http:{video}').content)
        videoRespond.close()

        print(f'{name} {list(videoRespond.json()["data"]["Component_Play_Playinfo"]["urls"])[0]} DOWNLOAD SUCCESSFUL.')