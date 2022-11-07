# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class PopularItem(scrapy.Item):
    # define the fields for your item here like:

    aid = scrapy.Field()  # 视频av号 aid
    tag_id = scrapy.Field()  # 视频tag_id tid
    tag_name = scrapy.Field()  # tag名字 tanme
    picture = scrapy.Field()  # 视频封面 pic
    title = scrapy.Field()  # 视频标题 title
    pubdate = scrapy.Field()  # 视频发布时的时间，为一个Unix时间戳
    ctime = scrapy.Field()  # 视频审核的时间，为一个Unix时间戳
    description = scrapy.Field()  # 视频简介 desc
    length = scrapy.Field()  # 视频长度（秒数）duration

    owner_mid = scrapy.Field()  # up主信息{ mid， name， face}
    owner_name = scrapy.Field()
    owner_face = scrapy.Field()

    # 以下信息在stat里面
    view = scrapy.Field()  # 播放数 view
    danmu = scrapy.Field()  # 弹幕数 danmuku
    reply = scrapy.Field()  # 评论数 reply
    favourite = scrapy.Field()  # 收藏数 favourite
    coin = scrapy.Field()  # 投币数 coin
    share = scrapy.Field()  # 分享数share
    like = scrapy.Field()  # 点赞数 like

    cid = scrapy.Field()    # 装填弹幕文件？
    link = scrapy.Field()  # 视频链接 short_link
    bvid = scrapy.Field()  # BV号
    reason = scrapy.Field()  # 推荐理由，可为空

    # 额外的信息：具体所属分区及其名字
    typeid = scrapy.Field()
    typename = scrapy.Field()


class PeopleItem(scrapy.Item):
    # 用户投稿视频总数
    count = scrapy.Field()

    mid = scrapy.Field()    # mid
    name = scrapy.Field()   # name
    sex = scrapy.Field()    # sex
    face = scrapy.Field()   # face
    birthday = scrapy.Field()    # birthday
    sign = scrapy.Field()   # sign

    following = scrapy.Field()
    follower = scrapy.Field()

    archive_view = scrapy.Field()
    article_view = scrapy.Field()
    likes = scrapy.Field()


class VideoItem(scrapy.Item):
    # noinspection HttpUrlsUsage
    """
        http://api.bilibili.com/x/web-interface/view?aid={}, 256219250
    """
    typeid = scrapy.Field()  # 视频标签种类id typeid
    typename = scrapy.Field()  # 视频所属的具体分区

    aid = scrapy.Field()  # 视频av号 aid
    bvid = scrapy.Field()  # 视频bv号，bvid

    tag_id = scrapy.Field()  # 视频tag_id tid
    tag_name = scrapy.Field()  # tag名字 tanme
    picture = scrapy.Field()  # 视频封面 pic
    title = scrapy.Field()  # 视频标题 title
    pubdate = scrapy.Field()  # 视频发布时的时间，为一个Unix时间戳
    ctime = scrapy.Field()  # 视频审核的时间，为一个Unix时间戳
    description = scrapy.Field()  # 视频简介 description
    length = scrapy.Field()  # 视频长度，在这里是一个H:m:s类型的字符串表示时间

    owner_mid = scrapy.Field()  # 保存up主的uid

    view = scrapy.Field()   # 视频播放数play
    danmu = scrapy.Field()  # 视频弹幕数
    reply = scrapy.Field()  # 评论数 reply
    favourite = scrapy.Field()  # 收藏数 favourite
    coin = scrapy.Field()  # 投币数 coin
    share = scrapy.Field()  # 分享数share
    like = scrapy.Field()  # 点赞数 like

    link = scrapy.Field()  # 自己添加一个视频链接

    cid = scrapy.Field()  # 装填弹幕文件？
