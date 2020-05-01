import requests
import json, re
from datetime import datetime


class ParseData():

    def parse_url(self, share_url):
        self.headers = {'User-Agent': 'AMAP_Location_SDK_Android 4.7.2'}
        self.url = 'https://v.douyin.com/' + re.findall('https://v.douyin.com/(.*?)/', share_url)[0] + "/"
        res = requests.get(self.url, headers=self.headers, allow_redirects=False)
        self.id = res.text.split('/')[5]
        self.mid = re.findall("mid=(.*?)&amp", res.text)[0]
        api = "https://www.iesdouyin.com/share/video/{}/".format(self.id)
        querystring = {"region": "CN", "mid": self.mid, "u_code": "14kfd7jc6", "titleType": "title",
                       "utm_source": "copy_link", "utm_campaign": "client_share", "utm_medium": "android",
                       "app": "aweme"}
        response = requests.request("GET", api, headers=self.headers, params=querystring)
        self.dytk = re.findall('dytk: "(.*?)"', response.text)[0]


    def get_data(self):
        api = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/"
        querystring = {"item_ids": self.id,
                       "dytk": self.dytk}
        response = requests.request("GET", api, headers=self.headers, params=querystring)
        js_data = json.loads(response.text)
        self.author_nickname = js_data['item_list'][0]['author']['nickname']
        self.author_avatar_addr = js_data['item_list'][0]['author']['avatar_medium']['url_list'][0]
        self.douyin_desc = js_data['item_list'][0]['desc']
        self.douyin_create_time = datetime.fromtimestamp(js_data['item_list'][0]['create_time'])
        self.author_unique_id = js_data['item_list'][0]['author']['short_id']
        self.author_signature = js_data['item_list'][0]['author']['signature']
        self.play_addr = js_data['item_list'][0]['video']['play_addr']['url_list'][0].replace('playwm','play')
        self.video_seconds = divmod(round(int(js_data['item_list'][0]['video']['duration'])/1000),60)
        self.video_duration = "%02d:%02d" % (self.video_seconds[0],self.video_seconds[1])
        self.v_length = int(js_data['item_list'][0]['video']['duration'])

    # def get_video_size(self):
    #     self.response = requests.get(self.play_addr, headers=self.headers)
    #     self.video_size = str(format(int(self.response.headers['Content-Length']) / 1048576, ".2f") + " Mb")
