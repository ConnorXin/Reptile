# -*- coding: utf-8 -*-
# @time    : 2023/9/2 13:37
# @author  : w-xin
# @file    : Bilibili_Sript_v1.py
# @software: PyCharm

"""
bilibili video
https://www.bilibili.com/video/BV1oj41127Jq
"""
import json
import re
from subprocess import run

import requests

if __name__ == '__main__':

    bilibili_url = 'https://www.bilibili.com/video/BV1oj41127Jq/?vd_source=d50d8d0ac0da0c11456a9b49f84c1718'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        'Cookie': "buvid3=09B10AF6-5C35-ABAE-1E5F-0E4B75A4217395559infoc;b_nut=100;buvid_fp_plain=undefined;i-wanna-go-back=-1;b_ut=7;buvid_fp=97549915ad78dba19080c9120f6b029a;fingerprint=4aa83c03ed3b8e405a86554057bf989f;bsource=search_baidu;_uuid=E66F13107-5D4E-2A4A-31DA-10228B64553AE52535infoc;b_lsid=D3F3A1084_18A542CC7A4;header_theme_version=CLOSE;home_feed_column=4;browser_resolution=1280-577;SESSDATA=daec1654%2C1709181371%2Cd24d1%2A92r5FBiTb4ahHPbVlngPXVxPNJkk6Bt1oUPTg2Y_VCrClPAEsQ1Vz6BPhM8ADlcGf1YEq0pwAALQA;bili_jct=42b7a3666035678412908d041b9d6b01;DedeUserID=356357045;DedeUserID__ckMd5=d337ddcc2d14a2a0;bp_video_offset_356357045=836448501582790678;buvid4=E46E7E8C-60D8-0845-2076-56E64B65B29696863-022062602-xjDxiKsyjbT5drk%2F3BOPnQ%3D%3D;CURRENT_FNVAL=4048;rpdid=|(k||RlmJJmY0J'uYmJYkmRku;bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTM4ODg2MjMsImlhdCI6MTY5MzYyOTQyMywicGx0IjotMX0.nCjk2sr3LNEv-HW9rfNVmtO8ZsOxlG290AmSwtxp6h4;bili_ticket_expires=1693888623;CURRENT_QUALITY=80;sid=gbhnokip;PVID=2",
        'Referer': bilibili_url
    }
    response = requests.get(url=bilibili_url, headers=header)

    text = response.text
    obj = re.compile(r'<script>window.__playinfo__=(?P<datas>.*?)</script>', re.S)
    video_datas = json.loads(obj.search(text).group('datas'))
    response.close()
    audio_url = video_datas['data']['dash']['audio'][0]['baseUrl']
    video_url = video_datas['data']['dash']['video'][0]['baseUrl']

    audio_response = requests.get(url=audio_url, headers=header)
    video_response = requests.get(url=video_url, headers=header)

    # to save
    with open('./未知计划_Pioneer0420.mp3', mode='wb') as f:
        f.write(audio_response.content)
    with open('./未知计划_Pioneer0420.mp4', mode='wb') as f:
        f.write(video_response.content)
    video_response.close()

    cmd_str = f'ffmpeg -i E:/github/Reptile/Get_Bilibili_Video/未知计划_Pioneer0420.mp4 -i E:/github/Reptile/Get_Bilibili_Video/未知计划_Pioneer0420.mp3 -c:v copy -c:a aac -strict experimental E:/github/Reptile/Get_Bilibili_Video/未知计划_Pioneer0420_output.mp4'
    run(cmd_str, shell=True)