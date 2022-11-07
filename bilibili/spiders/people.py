import scrapy, json
from bilibili import items


class PeopleSpider(scrapy.Spider):
    name = 'people'
    # uid = '161775300'
    uid = 36676936
    wait_time = 1
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://bilibili.com']

    def parse(self, response, **kwargs):
        # 程序从这开始，发送相应uid的请求去获取用户的信息
        info_url = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(self.uid)
        yield scrapy.Request(info_url, callback=self.myparse)

    def myparse(self, response):
        # 访问url以获取用户的基本信息
        text = json.loads(response.text)
        item = items.PeopleItem()
        item['mid'] = text['data']['mid']
        item['name'] = text['data']['name']
        item['sex'] = text['data']['sex']
        item['face'] = text['data']['face']
        item['birthday'] = text['data']['birthday']
        item['sign'] = text['data']['sign']
        item['count'] = 0
        meta = {
            'item': item,
        }
        fans_url = 'https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp'.format(self.uid)
        yield scrapy.Request(fans_url, callback=self.parse_user_fans, meta=meta)

    def parse_user_fans(self, response):
        """包括用户的粉丝数和关注数"""
        text = json.loads(response.text)
        item = response.meta['item']
        item['following'] = text['data']['following']
        item['follower'] = text['data']['follower']
        # 去获取用户的播放数、专栏阅读数
        url = 'https://api.bilibili.com/x/space/upstat?mid={}&jsonp=jsonp'.format(self.uid)
        meta = {
            'item': item,
        }
        yield scrapy.Request(url, callback=self.parse_user_stat, meta=meta)

    def parse_user_stat(self, response):
        """"""
        text = json.loads(response.text)
        item = response.meta['item']
        if text['data'] == {}:
            # 可能为空，没有设置相关cookie配置
            item['archive_view'] = 0
            item['article_view'] = 0
            item['like'] = 0
            # print("空字典！")
        else:
            item['archive_view'] = text['data']['archive']['view']
            item['article_view'] = text['data']['article']['view']
            item['likes'] = text['data']['likes']
        # 提交到管道
        yield item
