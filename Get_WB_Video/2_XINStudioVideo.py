# -*- coding: utf-8 -*-
# @Author  :  connor
# @Time    :  2023/8/15 15:43
# @File    :  2_XINStudioVideo.py
# @IDE     :  PyCharm

"""
XIN Studio
https://weibo.com/ajax/statuses/mymblog?uid=6303297939&page=1&feature=0
"""
import time
import traceback

import requests


if __name__ == '__main__':

    homeHeader = {
        'Cookie': 'XSRF-TOKEN=X_nNOg56fmKdhIz5egZ78nAL; _s_tentry=weibo.com; Apache=5568717781886.694.1692076041734; SINAGLOBAL=5568717781886.694.1692076041734; ULV=1692076041862:1:1:1:5568717781886.694.1692076041734:; SUB=_2A25J3028DeRhGeNH71MU8yzIzzqIHXVqrTh0rDV8PUNbmtAbLUj_kW9NSqHPYFAYqg8JZJQP6QfEcD8pZvPJJ5_l; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5yPX02GTP5aKL9fvaV9c4v5JpX5KzhUgL.Fo-4Sh2fe0zXShq2dJLoIp7LxKqL1KMLBoqLxK-LBo2LB.9ki--ciK.RiK.f; ALF=1723625835; SSOLoginState=1692089835; WBPSESS=gN4l19SPl2zPeLrUF3_e1TEmAVnasmPFhVucUcISh2uG2PDH6HH11SWRDeze7_-Eg92jueesdfTHyFmGuLbiy34u-2UCC0b5a9T5rS8CDipyc_-q6CcqQ_u3qGP1BLuNzpo47w6yA8KYKQKwZl-tKg==',
        'Referer': 'https://weibo.com/n/%E5%88%98%E9%9B%A8%E6%98%95%E5%B7%A5%E4%BD%9C%E5%AE%A4',
        'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Server-Version': 'v2023.08.15.1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Xsrf-Token': 'X_nNOg56fmKdhIz5egZ78nAL',
    }

    pageInfo = 1
    while True:
        try:
            if pageInfo != 1:
                homePageUrl = f'https://weibo.com/ajax/statuses/mymblog?uid=6303297939&page={pageInfo}&feature=0&since_id={since_id}'
            else:
                homePageUrl = f'https://weibo.com/ajax/statuses/mymblog?uid=6303297939&page={pageInfo}&feature=0'
            homeRespond = requests.get(url = homePageUrl, headers = homeHeader)

            since_id = homeRespond.json()['data']['since_id']
            contents = homeRespond.json()['data']['list']
            for content in contents:
                if 'url_struct' in content.keys():
                    for url_struct in content['url_struct']:
                        if '微博视频' in url_struct['url_title']:
                            dateSplit = content['created_at'].split(' ')[1: 3]
                            year = content['created_at'].split(' ')[-1]
                            dateSplit.append(year)
                            date = ' '.join(dateSplit)
                            if ':' in url_struct['actionlog']['oid']:
                                oid = url_struct['actionlog']['oid']
                            else:
                                oid = url_struct['long_url'].split('fid=')[1].split('&')[0]

                            videoHeader = {


                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                                'Referer': f'https://weibo.com/tv/show/{oid}',
                                'Cookie': 'XSRF-TOKEN=X_nNOg56fmKdhIz5egZ78nAL;_s_tentry=weibo.com;Apache=5568717781886.694.1692076041734;SINAGLOBAL=5568717781886.694.1692076041734;ULV=1692076041862:1:1:1:5568717781886.694.1692076041734:;SUB=_2A25J3028DeRhGeNH71MU8yzIzzqIHXVqrTh0rDV8PUNbmtAbLUj_kW9NSqHPYFAYqg8JZJQP6QfEcD8pZvPJJ5_l;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5yPX02GTP5aKL9fvaV9c4v5JpX5KzhUgL.Fo-4Sh2fe0zXShq2dJLoIp7LxKqL1KMLBoqLxK-LBo2LB.9ki--ciK.RiK.f;ALF=1723625835;SSOLoginState=1692089835;WBPSESS=gN4l19SPl2zPeLrUF3_e1TEmAVnasmPFhVucUcISh2uG2PDH6HH11SWRDeze7_-Eg92jueesdfTHyFmGuLbiy34u-2UCC0b5a9T5rS8CDipyc_-q6CcqQ_u3qGP1BLuNzpo47w6yA8KYKQKwZl-tKg==;PC_TOKEN=27b46779a9',
                                'Origin': 'https://weibo.com',
                                'Page-Referer': f'/tv/show/{oid}',
                                'Sec-Ch-Ua': '"Not/A)Brand";v="99","GoogleChrome";v="115","Chromium";v="115"',
                                'Sec-Ch-Ua-Mobile': '?0',
                                'Sec-Ch-Ua-Platform': '"Windows"',
                                'Sec-Fetch-Dest': 'empty',
                                'Sec-Fetch-Mode': 'cors',
                                'Sec-Fetch-Site': 'same-origin',
                                'X-Xsrf-Token': 'X_nNOg56fmKdhIz5egZ78nAL'
                            }
                            data = {
                                'data': '{"Component_Play_Playinfo": {"oid": "' + oid + '"}}'
                            }
                            videoUrl = f'https://weibo.com/tv/api/component?page={videoHeader["Page-Referer"]}'
                            videoRespond = requests.post(url = videoUrl, headers = videoHeader, data = data)
                            video = videoRespond.json()['data']['Component_Play_Playinfo']['urls'][list(videoRespond.json()['data']['Component_Play_Playinfo']['urls'])[0]]
                            title = videoRespond.json()['data']['Component_Play_Playinfo']['title'].replace('\n', '').replace('| ', '').replace('|', '')

                            with open(f'./XIN/Studio/{date}_{title}.mp4', mode='wb') as f:
                                f.write(requests.get(f'http:{video}').content)
                            videoRespond.close()

                            print(f'{title} {list(videoRespond.json()["data"]["Component_Play_Playinfo"]["urls"])[0]} download successful.')
                time.sleep(2)
            homeRespond.close()

            print('-' * 60)
            print(f'page {pageInfo} retrive successful.')
            print('-' * 60)
            pageInfo += 1
            time.sleep(2)
        except:
            print(videoUrl)
            traceback.print_exc()