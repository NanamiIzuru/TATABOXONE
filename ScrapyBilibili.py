import crochet
import json
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from bilibili.spiders import people, video
from app01 import models


class Finish:
    Popular_flag = False
    People_flag = False
    Video_flag = False


def get_popular():
    # 执行爬虫之前先把表给清空
    models.PopularInfo.objects.all().delete()

    Finish.Popular_flag = True
    crochet.setup()
    setting = get_project_settings()
    process = CrawlerRunner(setting)
    process.crawl('popular')
    # 等待执行结束
    while Finish.Popular_flag:
        continue


def get_peoson(uid=36676936):
    print("爬取用户uid={}!".format(uid))
    people.PeopleSpider.uid = uid

    Finish.People_flag = True
    crochet.setup()
    setting = get_project_settings()
    process = CrawlerRunner(setting)
    process.crawl('people')

    # 等待执行结束
    while Finish.People_flag:
        continue


def get_video(uid=36676936):
    # 先去看一下people表中是否存在当前uid的用户，若不存在先爬取用户
    result = models.PeopleInfo.objects.filter(mid=uid).exists()
    if not result:
        print("视频爬虫：用户不存在！先爬取用户！")
        get_peoson(uid)
    else:
        print("视频爬虫：用户存在，可以爬取！")
    video.VideoSpider.uid = uid
    # 开始爬虫前，先设置标记位
    Finish.Video_flag = True
    crochet.setup()
    setting = get_project_settings()
    process = CrawlerRunner(setting)
    process.crawl('video')

    # 等待执行结束
    while Finish.Video_flag:
        continue

def find_type_name(s):
    with open("myConfig.json", "r", encoding='utf-8') as f:
        dic = json.load(f)
        try:
            s = dic['typename'][s]
            return s, dic['typeid'][s]
        except BaseException:
            print("str不存在！")
            return False, False
