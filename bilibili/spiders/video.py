import scrapy
import json
from bilibili import items
from app01 import models


class VideoSpider(scrapy.Spider):
    name = 'video'
    # uid = '161775300'
    uid = 36676936
    total_video_num = 0
    ps = 50
    # allowed_domains = ['bilibili.com']
    start_urls = ['http://bilibili.com/']
    video_url = "http://api.bilibili.com/x/web-interface/view?aid={}"

    def parse(self, response, **kwargs):
        url = 'https://api.bilibili.com/x/space/arc/search?' \
              'mid={}&ps={}&tid=0&pn=1&order=pubdate&jsonp=jsonp'.format(self.uid, self.ps)
        yield scrapy.Request(url, callback=self.myparse)
        pass

    def myparse(self, response):
        """
        先获取每一种视频的类别，再去爬取每一种分类下有什么视频
        :param response:
        :return:
        """
        # 先爬取用户的视频数量
        text = json.loads(response.text)
        # print(text)
        self.total_video_num = text['data']['page']['count']
        print("该用户UID为：{}, 投稿视频总数为：{}".format(self.uid, text['data']['page']['count']))
        models.PeopleInfo.objects.filter(mid=int(self.uid)).update(count=self.total_video_num)
        # 获取到类别后，根据类别分类去爬取具体分区，这里的分区是大区分区
        type_list = text['data']['list']['tlist']
        # type_list不为空才继续爬取
        if type_list:
            # type_list 类型：一个字典套字典
            # {'181': {'tid': 181, 'count': 1, 'name': '影视'}, '4': {'tid': 4, 'count': 4, 'name': '游戏'}}
            url = "https://api.bilibili.com/x/space/arc/search?mid={}&ps={}&tid={}&pn={}&order=pubdate"
            for k, v in type_list.items():
                # v是一个字典，访问字典中的tid， 或者直接使用k的值作为tid, 然后先访问第一页
                real_url = url.format(self.uid, self.ps, k, 1)
                meta = {
                    'tid': v['tid'],
                    'tname': v['name'],
                    'count': v['count'],
                }
                print("{}下的视频列表：{}".format(v['name'], real_url))
                yield scrapy.Request(real_url, callback=self.parse_detail, meta=meta)

    def parse_detail(self, response):
        """在这里获取每个分区下的所有视频"""
        tid = response.meta['tid']
        tname = response.meta['tname']
        count = response.meta['count']
        print("分区id：{}, 分区标签：{}, 数量：{}".format(tid, tname, count))
        # 定义视频item，并把相应的分区标签写到视频里

        text = json.loads(response.text)
        video_list = text['data']['list']['vlist']
        for i in video_list:
            # print("分区：{}, av号：{}, 标题：{}".format(tname, i['aid'], i['title']))
            video_item = items.VideoItem()
            video_item['typeid'] = tid
            video_item['typename'] = tname
            real_url = self.video_url.format(i['aid'])
            meta = {
                'item': video_item
            }
            # time.sleep(self.wait_time)
            # 然后对视频的详细信息进行请求
            yield scrapy.Request(real_url, callback=self.parse_video, meta=meta)

        # 判断是否需要继续跟进
        num = 1
        url = "https://api.bilibili.com/x/space/arc/search?mid={}&ps=50&tid={}&pn={}&order=pubdate"
        meta = {
            'tid': tid,
            'tname': tname
        }
        while num*50 < count:
            # 视频还有多的页，需要继续跟进，把当前页的tid和tname打包发送过去
            num += 1
            real_url = url.format(self.uid, tid, num)
            print("继续跟进url：{}".format(real_url))
            yield scrapy.Request(real_url, callback=self.parse_more, meta=meta)

    def parse_more(self, response):
        text = json.loads(response.text)
        tid = response.meta['tid']
        tname = response.meta['tname']

        video_list = text['data']['list']['vlist']
        for i in video_list:
            # print("分区：{}, av号：{}, 标题：{}".format(tname, i['aid'], i['title']))
            video_item = items.VideoItem()
            video_item['typeid'] = tid
            video_item['typename'] = tname
            real_url = self.video_url.format(i['aid'])
            meta = {
                'item': video_item
            }
            # time.sleep(self.wait_time)
            # 然后对视频的详细信息进行请求
            yield scrapy.Request(real_url, callback=self.parse_video, meta=meta)

    def parse_video(self, response):
        text = json.loads(response.text)['data']
        item = response.meta['item']
        # 对剩下的内容进行解析
        item['bvid'] = text['bvid']
        item['aid'] = text['aid']
        item['tag_id'] = text['tid']
        item['tag_name'] = text['tname']
        item['picture'] = text['pic']
        item['title'] = text['title']
        item['pubdate'] = text['pubdate']
        item['ctime'] = text['ctime']
        item['description'] = text['desc']
        item['length'] = text['duration']
        item['owner_mid'] = text['owner']['mid']

        item['view'] = text['stat']['view']
        item['danmu'] = text['stat']['danmaku']
        item['reply'] = text['stat']['reply']
        item['favourite'] = text['stat']['favorite']
        item['coin'] = text['stat']['coin']
        item['share'] = text['stat']['share']
        item['like'] = text['stat']['like']

        item['link'] = "https://b23.tv/"+text['bvid']

        item['cid'] = text['cid']

        yield item
