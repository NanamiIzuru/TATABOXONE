# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

from bilibili import items
from app01 import models

import ScrapyBilibili


class PopularPipeline:

    def open_spider(self, spider):
        print("开始爬虫！")

    def process_item(self, item, spider):
        if not isinstance(item, items.PopularItem):
            # print("不是Popularitem，经过")
            return item
        try:
            typename, typeid= ScrapyBilibili.find_type_name(item['tag_name'])
            if typename:
                item['typename'] = typename
                item['typeid'] = typeid
        except:
            pass

        models.PopularInfo.objects.create(
            aid=item['aid'],
            bvid=item['bvid'],
            cid=item['cid'],
            coin=item['coin'],
            ctime=item['ctime'],
            danmu=item['danmu'],
            description=item['description'],
            favourite=item['favourite'],
            length=item['length'],
            like=item['like'],
            link=item['link'],
            owner_face=item['owner_face'],
            owner_mid=item['owner_mid'],
            owner_name=item['owner_name'],
            picture=item['picture'],
            pubdate=item['pubdate'],
            reason=item['reason'],
            reply=item['reply'],
            share=item['share'],
            tag_id=item['tag_id'],
            tag_name=item['tag_name'],
            title=item['title'],
            type_id=item['typeid'],
            type_name=item['typename'],
            view=item['view']
        )
        # print(item)
        print(item)
        return item

    def close_spider(self, spider):
        ScrapyBilibili.Finish.Popular_flag = False
        print("结束爬虫！")


class PeoplePipeline:
    def process_item(self, item, spider):
        if not isinstance(item, items.PeopleItem):
            # print("不是PeopleItem，经过")
            return item
        people = models.PeopleInfo.objects.filter(mid=item['mid']).first()
        if people:
            # 若存在相关数据，则更新相关数据
            people.archive_view = item['archive_view']
            people.article_view = item['article_view']
            people.birthday = item['birthday']
            people.count = item['count']
            people.face = item['face']
            people.follower = item['follower']
            people.following = item['following']
            people.likes = item['likes']
            people.mid = item['mid']
            people.name = item['name']
            people.sex = item['sex']
            people.sign = item['sign']
            people.save()
        else:
            # 否则对数据进行添加
            models.PeopleInfo.objects.create(
                archive_view=item['archive_view'],
                article_view=item['article_view'],
                birthday=item['birthday'],
                count=item['count'],
                face=item['face'],
                follower=item['follower'],
                following=item['following'],
                likes=item['likes'],
                mid=item['mid'],
                name=item['name'],
                sex=item['sex'],
                sign=item['sign']
            )
        print(item)
        return item

    def close_spider(self, spider):
        ScrapyBilibili.Finish.People_flag = False


class VideoPipeline:

    def process_item(self, item, spider):
        if not isinstance(item, items.VideoItem):
            # print("不是VideoItem，经过")
            return item
        video = models.VideoInfo.objects.filter(aid=item['aid']).first()
        # 若存在，则更新相关数据
        if video:
            video.aid = item['aid']
            video.bvid = item['bvid']
            video.cid = item['cid']
            video.coin = item['coin']
            video.ctime = item['ctime']
            video.danmu = item['danmu']
            video.description = item['description']
            video.favourite = item['favourite']
            video.length = item['length']
            video.like = item['like']
            video.link = item['link']
            video.owner_mid = item['owner_mid']
            video.picture = item['picture']
            video.pubdate = item['pubdate']
            video.reply = item['reply']
            video.share = item['share']
            video.tag_id = item['tag_id']
            video.tag_name = item['tag_name']
            video.title = item['title']
            video.type_id = item['typeid']
            video.type_name = item['typename']
            video.view = item['view']
            video.save()
        else:
            # 否则新建一条新信息
            models.VideoInfo.objects.create(
                aid=item['aid'],
                bvid=item['bvid'],
                cid=item['cid'],
                coin=item['coin'],
                ctime=item['ctime'],
                danmu=item['danmu'],
                description=item['description'],
                favourite=item['favourite'],
                length=item['length'],
                like=item['like'],
                link=item['link'],
                owner_mid=item['owner_mid'],
                picture=item['picture'],
                pubdate=item['pubdate'],
                reply=item['reply'],
                share=item['share'],
                tag_id=item['tag_id'],
                tag_name=item['tag_name'],
                title=item['title'],
                type_id=item['typeid'],
                type_name=item['typename'],
                view=item['view']
            )
        print(item)
        return item

    def close_spider(self, spider):
        ScrapyBilibili.Finish.Video_flag = False

# class ImgsPipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         print(item["picture"])
#         yield scrapy.Request(item["picture"])
#
#     def file_path(self, request, response=None, info=None, *, item=None):
#         imgName = request.url.split('/')[-1]
#         return imgName
#
#     def item_completed(self, results, item, info):
#         return item
