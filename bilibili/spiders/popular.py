import scrapy
import json

from bilibili.items import PopularItem
import time


def fill_item(item, info):
    item['aid'] = info['aid']
    item['tag_id'] = info['tid']
    item['tag_name'] = info['tname']
    item['picture'] = info['pic']
    item['title'] = info['title']
    item['pubdate'] = info['pubdate']
    item['ctime'] = info['ctime']
    item['description'] = info['desc']
    item['length'] = info['duration']

    item['owner_mid'] = info['owner']['mid']
    item['owner_name'] = info['owner']['name']
    item['owner_face'] = info['owner']['face']

    item['view'] = info['stat']['view']
    item['danmu'] = info['stat']['danmaku']
    item['reply'] = info['stat']['reply']
    item['favourite'] = info['stat']['favorite']
    item['coin'] = info['stat']['coin']
    item['share'] = info['stat']['share']
    item['like'] = info['stat']['like']

    item['cid'] = info['cid']
    item['link'] = info['short_link']
    item['bvid'] = info['bvid']
    item['reason'] = info['rcmd_reason']['content']

    item['typeid'] = 0
    item['typename'] = ""


class PopularSpider(scrapy.Spider):
    name = 'popular'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://api.bilibili.com/x/web-interface/popular?ps=50&pn=1']
    url = 'https://api.bilibili.com/x/web-interface/popular?ps=50&pn={}'
    num = 2
    wait_time = 1
    def parse(self, response, **kwargs):
        text = json.loads(response.text)
        for i in range(50):
            info = text['data']['list'][i]
            item = PopularItem()
            fill_item(item, info)
            yield item
        while self.num <= 4:
            time.sleep(self.wait_time)
            new_url = self.url.format(self.num)
            self.num += 1
            yield scrapy.Request(url=new_url, callback=self.parse)
