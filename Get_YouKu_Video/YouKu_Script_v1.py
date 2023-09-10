# -*- coding: utf-8 -*-
# @time    : 2023/9/9 16:15
# @author  : w-xin
# @file    : YouKu_Script_v1.py
# @software: PyCharm

"""
一步一步运行程序
"""
import base64
import json
import re
import subprocess
import time
from hashlib import md5

import requests


class YouKu:

    def __init__(self, cookie):

        self.cookie = cookie


    def youku_sign(self, t, data, token):
        appKey = '24679788'     # 固定值
        '''token值在cookie中'''
        sign = token + '&' + t + '&' + appKey + '&' + data
        md = md5()
        md.update(sign.encode('UTF-8'))
        sign = md.hexdigest()
        return sign


    def utid(self):
        """
        get cna and token
        :return: cna and token dict
        """
        cna = re.compile("cna=(.*?);")
        _m_h5_tk = re.compile("_m_h5_tk=(.*?)_.*?;")
        token = _m_h5_tk.findall(self.cookie+";")
        utid_ = cna.findall(self.cookie+";")
        return {"utid": utid_[0], "token": token[0]}


    # 若直接在首页小窗口上复制的视频网址，是重定向的网址。
    def redirect(self, url):
        """
        视频网址请求
        :param url: 视频网址
        :return: 响应视频网址
        """
        headers = {
            'referer': 'https://www.youku.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        resp = requests.get(url=url, headers=headers)
        return resp.url


    def page_parser(self, url):
        """
        get video id, show id, encode video id
        :param url: video link
        :return: video id, show id, encode video id: dict
        """
        headers = {
            "authority": "v.youku.com",
            "method": "GET",
            "path": url.replace("https://v.youku.com", ""),
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Cookie": self.cookie,
            "Referer": "https://www.youku.com/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        resp = requests.get(url=url, headers=headers)
        html = resp.content.decode("utf-8")
        # html = resp.text
        print(resp)
        videoId = re.compile("videoId: '(?P<id>.*?)'", re.S)
        showid = re.compile("showid: '(?P<id>.*?)'", re.S)
        currentEncodeVid = re.compile("currentEncodeVid: '(?P<id>.*?)'", re.S)
        # videoId = re.compile("videoId: '(.*?)'")
        # showid = re.compile("showid: '(.*?)'")
        # currentEncodeVid = re.compile("currentEncodeVid: '(.*?)'")
        # videoId = videoId.search(html).group('id')
        videoId = videoId.search(html).group('id')
        current_showid = showid.search(html).group('id')
        vid = currentEncodeVid.search(html).group('id')
        # ['1488104108'] ['558712'] ['XNTk1MjQxNjQzMg==']
        print(videoId, current_showid, vid)

        return {"current_showid": current_showid, "videoId": videoId, "vid": vid}


    def get_emb(self, videoId):
        """
        得到 Base64 编码的字符串
        :param videoId:
        :return:
        """
        emb = base64.b64encode((f"{videoId}www.youku.com/").encode('utf-8')).decode('utf-8')
        return emb


    def takeOne(self, elem):
        """
        get the first element
        :param elem:
        :return:
        """
        return float(elem[0])


    def m3u8_url(self, t, params_data, sign):

        url = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/'

        params = {
            "jsv": "2.6.1",
            "appKey": "24679788",
            "t": t,
            "sign": sign,
            "api": "mtop.youku.play.ups.appinfo.get",
            "v": "1.1",
            "timeout": "15000",
            # "YKPid": "20160317PLF000211",
            # "YKLoginRequest": "true",
            "AntiFlood": "true",
            "AntiCreep": "true",
            "type": "jsonp",
            "dataType": "jsonp",
            "callback": "mtopjsonp1",
            "data": params_data,
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Cookie": self.cookie,
            "Host": "acs.youku.com",
            "Referer": "https://v.youku.com/v_show/id_XNTk1MjQxNjQzMg==.html?spm=a2hja.12701310.filter.37&s=aabd0d1709214ada89a3&s=aabd0d1709214ada89a3",
            'Sec-Ch-Ua': '"Chromium";v="116","Not)A;Brand";v="24","GoogleChrome";v="116"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-site",
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        url = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv=2.6.1&appKey=24679788&t=1694261214310&sign=4422ee1eaa276e2c28588719afe2e17a&api=mtop.youku.play.ups.appinfo.get&v=1.1&timeout=15000&AntiFlood=true&AntiCreep=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22steal_params%22%3A%22%7B%5C%22ccode%5C%22%3A%5C%220502%5C%22%2C%5C%22utid%5C%22%3A%5C%22JeHjG%2BALXRkCAX1b9P7tA6IX%5C%22%2C%5C%22version%5C%22%3A%5C%229.4.26%5C%22%2C%5C%22ckey%5C%22%3A%5C%22140%23cpfoFecczzWktzo23zJz4pN8s9xiId6TXKuyQQIUFNHplIT8DVCKklMNlmx088DhIVbLR3hqzznJgR4osBzzzZFhbjvqlQzx2DD3VthqzF4N2FXdlp1xzoObV2EqlVOnpKII1wba7X5mDxfjGNBxKWr6xkgw96XUoQKgCpuULB0hrxew4KBba6EBNLNqzNsDRooX3fzawhWwN75NRlOjV9gNN0RK4PB%2Bqb3AGoHiV3cNZbo5kaaUb3bih95E8nczSawfvZMJMAVj1dx48%2FkE1NiyUjHGgsVDTOqcX%2FxqYOAmFF203nK9qr9JMGeirPf3AYfkoIYgC7P%2BfJCds07q7uGn7HzxiSVZ19Q%2F7DDfzhll1giBPMN1B58VAKPOrahkuFonYNuMRuGYjiduiB8HmGlJrEg8Hmvqj69%2BL9weIGgwua1y0IO8wTf8C2CMxeLtDLmZ8%2BY9QfVGV0tk%2FNf%2F7NzoGS%2BOC4qAsAu2lcnc7goZ98%2FZXj2ODluBQngw%2BRhzznIxLirqENhFfULEP1h150KIc0sCkv1KACUtKt5lD7lIYooDLiuUCLmVpWLpXEN30w1ne3pX3Qh%2FnqAPX%2FXNR3txP0Ocpy52SjxWYKBQAKVfsa0rWzEFslJArSmapfQg%2FOzv3BD2EQefyP8ZKGz3CiGAjleOqq94LDW7wTlMxnX3l079Kifdo5humAXb24Jldh1FcDvN%2FkKmmftzzfqFJUe0c54onUbRo0Em6x2c9qdnNkiuH3KU%2FONP9gi5sQlcPuxdtxoixVT85O4tN5z%3D%5C%22%2C%5C%22client_ip%5C%22%3A%5C%22192.168.1.1%5C%22%2C%5C%22client_ts%5C%22%3A1694261213%7D%22%2C%22biz_params%22%3A%22%7B%5C%22vid%5C%22%3A%5C%22XNTk1MjQxNjQzMg%3D%3D%5C%22%2C%5C%22h265%5C%22%3A0%2C%5C%22current_showid%5C%22%3A%5C%22558712%5C%22%2C%5C%22preferClarity%5C%22%3A4%2C%5C%22media_type%5C%22%3A%5C%22standard%2Csubtitle%5C%22%2C%5C%22app_ver%5C%22%3A%5C%229.4.26%5C%22%2C%5C%22extag%5C%22%3A%5C%22EXT-X-PRIVINF%5C%22%2C%5C%22play_ability%5C%22%3A16782592%2C%5C%22master_m3u8%5C%22%3A1%2C%5C%22drm_type%5C%22%3A19%2C%5C%22key_index%5C%22%3A%5C%22web01%5C%22%2C%5C%22encryptR_client%5C%22%3A%5C%22FXWfIDRVI8a9o24sTUMLyg%3D%3D%5C%22%2C%5C%22local_vid%5C%22%3A%5C%22XNTk1MjQxNjQzMg%3D%3D%5C%22%2C%5C%22local_time%5C%22%3A1694248950%2C%5C%22skh%5C%22%3A1%2C%5C%22start_point_ms%5C%22%3A377611%2C%5C%22last_clarity%5C%22%3A3%2C%5C%22clarity_chg_ts%5C%22%3A1692463698%7D%22%2C%22ad_params%22%3A%22%7B%5C%22vs%5C%22%3A%5C%221.0%5C%22%2C%5C%22pver%5C%22%3A%5C%229.4.26%5C%22%2C%5C%22sver%5C%22%3A%5C%222.0%5C%22%2C%5C%22site%5C%22%3A1%2C%5C%22aw%5C%22%3A%5C%22w%5C%22%2C%5C%22fu%5C%22%3A0%2C%5C%22d%5C%22%3A%5C%220%5C%22%2C%5C%22bt%5C%22%3A%5C%22pc%5C%22%2C%5C%22os%5C%22%3A%5C%22win%5C%22%2C%5C%22osv%5C%22%3A%5C%2210%5C%22%2C%5C%22dq%5C%22%3A%5C%22hd2%5C%22%2C%5C%22atm%5C%22%3A%5C%22%5C%22%2C%5C%22partnerid%5C%22%3A%5C%22null%5C%22%2C%5C%22wintype%5C%22%3A%5C%22interior%5C%22%2C%5C%22isvert%5C%22%3A0%2C%5C%22vip%5C%22%3A0%2C%5C%22emb%5C%22%3A%5C%22%5C%22%2C%5C%22p%5C%22%3A1%2C%5C%22rst%5C%22%3A%5C%22mp4%5C%22%2C%5C%22needbf%5C%22%3A2%2C%5C%22avs%5C%22%3A%5C%221.0%5C%22%7D%22%7D'
        # resp = requests.get(url=url, params=params, headers=headers)
        resp = requests.get(url=url, headers=headers)
        result =resp.text
        print(result[11: -1])
        # data = json.loads(result[11: -1])
        # print(data)
        # ret = data["ret"]
        # video_lists = []
        # if ret == ["SUCCESS::调用成功"]:
        #     stream = data["data"]["data"]["stream"]
        #     title = data["data"]["data"]["video"]["title"]
        #     print("解析成功:")
        #     for video in stream:
        #         m3u8_url = video["m3u8_url"]
        #         width = video["width"]
        #         height = video["height"]
        #         size = video["size"]
        #         size = '{:.1f}'.format(float(size) / 1048576)
        #         video_lists.append([size, width, height, title, m3u8_url])
        #         # print(f">>>  {title} 分辨率:{width}x{height} 视频大小:{size}M \tm3u8播放地址:{m3u8_url}")
        #
        #     video_lists.sort(key=self.takeOne)
        #     for video_list in video_lists:
        #         print(f">>>  {title} 分辨率:{video_list[1]}x{video_list[2]} 视频大小:{video_list[0]}M \tm3u8播放地址:{video_list[4]}")
        #     # self.play(video_lists[-1][4])    # 选择播放列表最后一个视频（经过sort排序后，最后一个即为清晰度最高的一个）
        # elif ret == ["FAIL_SYS_ILLEGAL_ACCESS::非法请求"]:
        #     print("请求参数错误")
        # elif ret == ["FAIL_SYS_TOKEN_EXOIRED::令牌过期"]:
        #     print("Cookie过期")
        # else:
        #     print(ret[0])


    def play(self, x):
        text = 'ffplay -protocol_whitelist "file,http,https,rtp,udp,tcp,tls" -loglevel quiet -i "%s"' % x
        subprocess.call(text, shell=True)


    def start(self):
        """
        start code
        :return:
        """
        # while True:
        # try:
        t = str(int(time.time() * 1000))
        user_info = self.utid()
        userid = user_info["utid"]
        url = 'https://v.youku.com/v_show/id_XNTk1MjQxNjQzMg==.html?spm=a2hja.12701310.filter.37&s=aabd0d1709214ada89a3&s=aabd0d1709214ada89a3'
        # url = input("\n\n请将优酷视频播放链接粘贴到这:\n")
        url = self.redirect(url)
        page_info = self.page_parser(url)
        emb = self.get_emb(page_info["videoId"])
        # params_data = r'''{"steal_params":"{\"ccode\":\"0502\",\"client_ip\":\"192.168.1.1\",\"utid\":\"%s\",\"client_ts\":%s,\"version\":\"2.1.69\",\"ckey\":\""}","biz_params":"{\"vid\":\"%s\",\"play_ability\":16782592,\"current_showid\":\"%s\",\"preferClarity\":99,\"extag\":\"EXT-X-PRIVINF\",\"master_m3u8\":1,\"media_type\":\"standard,subtitle\",\"app_ver\":\"2.1.69\",\"h265\":1}","ad_params":"{\"vs\":\"1.0\",\"pver\":\"2.1.69\",\"sver\":\"2.0\",\"site\":1,\"aw\":\"w\",\"fu\":0,\"d\":\"0\",\"bt\":\"pc\",\"os\":\"win\",\"osv\":\"10\",\"dq\":\"auto\",\"atm\":\"\",\"partnerid\":\"null\",\"wintype\":\"interior\",\"isvert\":0,\"vip\":1,\"emb\":\"%s\",\"p\":1,\"rst\":\"mp4\",\"needbf\":2,\"avs\":\"1.0\"}"}'''% (userid, t[:10], page_info["vid"], page_info["current_showid"], emb)
        params_data = r'''{\"steal_params": "{\"ccode\":\"0502\",\"utid\":\"%s\",\"version\":\"9.4.26\",\"ckey\":\"140#xqsDRDkIzzFxJzo2+ixQ4pN8s9xiSlEsbuLEK+WgAMehH9c6FLuFWLYl07xNKtDkKQholp1zzqgTcE8riFzx0Hjd7th/zzrb22U3lp1xz9O03VzLxzrz2PzvL6hqzFx6dZz/OSvZrI7Zb6itG1Kf2joCFLdGioytTexxP4secKSiB9iYajxMenNddkxiansPim2/AATBH6fG9c0daD+jB119xg50qoZkOaujZGgkx98jQnKW1wdNp+nU2fXdMhn9WGIRtuG21+cfGFCSoGQUFD9Bp3jYJcGvqiaKvkYYRS16LmSYBaF3OnX9vMNmx6gZowmOAPI6L3fQ1DE+k9Gd7XGwdk+lH7gXgY3XnCFmtvCKWuwpFUT5sdxHOxTDK2oqC1vcUGs5+FsGGnV7RujrEPfcSdf5bP70v+sCsNs6DflwzZQwEAJvxEe3DoOB0SCItnGPe/oG5GKjakadjc7o3fwCsL588r08yj6p0QzOBw2OK4z9XLoC1WNMCWrabLGzMvdlzt7HHqGyTksPw6JxeJyivBO5Gr2TE4LGd5qPEQ6tMQmuSAsFZtAbnYS3XnxUtKXL5B8OSZ/6IVOtAR8HM89vDOCkQq5mnKnPC7u99Czc2iVFgcQNluVnc8BPVDBaSbrqS9cXrcFgADCBVDES7EX9gul5QgpZox8WEOCyNW0CmWYnYatKyDdbWKbeOwutXiLZiU0EueR2hFSpyyRVADrXhaVhEWV72EucmELeukVzd5NecsI4oAQEUWx0haW+TxEwehvAg8CiuRg0eFmDlk0huIersbKkeAcutJiMtEb4/rWmYDZxbwWsYMoghUL1U6pyBww1AYL6+6pt0XzvdP6bUznI6EJbNC/b3Xl2FAjqHckUVDfiAsvVse80kxt7iNZLJAm7HyTuT4qyJLkKubpY5KxpgOt6GAhBEuAY8WWqgKT2LUtayNBHNRKBtjuNEZq7uj9JslOJWdnkkcQc+QmuEbrXUurScLA+K6r9829xNxMtRlYHyUoSoTiYSnYoKMtmuldGRrPFpBpQKPIO85Fl3kWvtVnAX/QGL6dAfXzF/qYA47gkwaE4yWWWetsmxG5g638t4nrtF2z9XXcZwkCHl5YuKJeAyiVjiDs4kSyeJa68UlABaZDgBvaC8Haw2uZlCschjiPtJ2FUwWcHCYYkuSK3x+axx2OiFnVyXzz=\",\"client_ip\":\"192.168.1.1\",\"client_ts\":%s}","biz_params": "{\"vid\":\"%s\",\"h265\":0,\"current_showid\":\"%s\",\"preferClarity\":4,\"media_type\":\"standard,subtitle\",\"app_ver\":\"9.4.26\",\"extag\":\"EXT-X-PRIVINF\",\"play_ability\":16782592,\"master_m3u8\":1,\"drm_type\":19,\"key_index\":\"web01\",\"encryptR_client\":\"CugEReCHhQBs92xtcq2Z9g==\",\"local_vid\":\"%s\",\"local_time\":%s,\"skh\":1,\"start_point_ms\":926992,\"last_clarity\":3,\"clarity_chg_ts\":%s}","ad_params": "{\"vs\":\"1.0\",\"pver\":\"9.4.26\",\"sver\":\"2.0\",\"site\":1,\"aw\":\"w\",\"fu\":0,\"d\":\"0\",\"bt\":\"pc\",\"os\":\"win\",\"osv\":\"10\",\"dq\":\"hd2\",\"atm\":\"\",\"partnerid\":\"null\",\"wintype\":\"interior\",\"isvert\":0,\"vip\":0,\"emb\":\"\",\"p\":1,\"rst\":\"mp4\",\"needbf\":2,\"avs\":\"1.0\"}"}''' % (userid, t[: 10], page_info['vid'], page_info['current_showid'], page_info['vid'], t[: 10], t[: 10])
        sign = self.youku_sign(t, params_data, user_info["token"])
        # self.m3u8_url(t, params_data, sign)
        # except Exception as e:
        #     print('error:', e, "或可能cookie设置错误")
                # break


if __name__ == '__main__':

    print('=' * 35 + '>> 欢迎使用优酷视频m3u8地址解析工具 <<' + '=' * 35)
    cookie = 'cna=JeHjG+ALXRkCAX1b9P7tA6IX;__ysuid=1667035942038241;isI18n=false;__ayft=1692439967340;P_F=1;__arycid=dd-3-00;__arcms=dd-3-00;P_ck_ctl=A21573818DC75C0C166F0F5A32D8BC86;P_gck=NA%7CiUoDkof81BDdChyH4%2B1WtQ%3D%3D%7CNA%7C1692463223907;P_pck_rm=hhfLngbq0f5b0d8de9825eZB1T52EqV7hoQ3X%2BTk%2FH0u5cDvGYniYvOApnLtoCty5vrigmlPrC6MjWZGVo8GfXxwU%2FFnS%2BQhg1mkKIQvLXogknd5uCUU88kauMEwV3jmsweQO6mO5QNrl8O1%2B6bzz4tBfzdEHMHmcNbP4g%3D%3D%5FV2;disrd=27914;youku_history_word=["%E6%B6%88%E5%A4%B1%E7%9A%84%E7%97%95%E8%BF%B9"];__aysid=1694244383930Rfo;__ayscnt=4;xlly_s=1;_m_h5_tk=b34b564a002489958245d6bb1f9e56cb_1694264029542;_m_h5_tk_enc=c289beff88c7db61ea4b21e3e20f20c7;__ayvstp=83;__aysvstp=18;__arpvid=1694264982137yyoWIu-1694264982156;__aypstp=36;__ayspstp=7;x5sec=7b22617365727665722d686579693b32223a226331383236353234373238636634356262356564646564303663653533333436434a626438616347454b6541773533372f2f2f2f2f774577676f48777a766a2f2f2f2f2f41554144222c22733b32223a2232636230313733343065306334656438227d;tfstk=dbzMzTXW6loscvmvMh31S5HM9Tjdfdgbu-LxHqHVYvkBDm-tWEW0wvUtB53aKnrUG-H9WV7mikrZcEwtbys0D5obMctYRKcKtmyxH5C0KkrCCO_sHrc0Ykwmc1Mx3x2YglCdyaF_1qg4nTQRyJ_4yQf-VcO_K5gjuTdpugQu18OEDMjsqLj7bHaFsmMkMuTIwdvnEYPZQ5FT8gn9fWDHuEz3xcXNAH-yqSTjTsUecniZOXD-EA9m8;l=fBLecD1PN9OtN87QKO5Z-urza77OVIdfCsPzaNbMiIEGa6OPsFTzXNC6Jtkv-dtjgTCA1etyVhmX9dQZ63Up4xDDBe0crmhnnxvtaQtJe;isg=BEBAOD2yMP8YAMzn_2UAKhtlEc4SySSTXqN2PLrQo9vuNeVfYtmxImMHTZ31hdxr'
    # cookie = input("\n使用前,请设置优酷的cookie:\n")
    # print("\n这是一个循环：可以不停的解析...")
    youku = YouKu(cookie)
    youku.start()
