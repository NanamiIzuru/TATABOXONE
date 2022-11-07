from django.db import models
# Create your models here.


class UserInfo(models.Model):
    """
    create table app01_userinfo(
        id bigint auto_increment primary key
        name  varchar(32)
        password  varchar(32)
        age int
    )
    """
    name = models.CharField(verbose_name="姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)
    age = models.IntegerField(verbose_name="年龄")


class PrettyNum(models.Model):
    """"""
    mobile = models.CharField(verbose_name="手机号码", max_length=11)
    price = models.DecimalField(verbose_name="价格", default=0, max_digits=10, decimal_places=2)
    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
        (5, "5级")
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = (
        (0, "未占用"),
        (1, "已使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=0)


class PopularInfo(models.Model):
    aid = models.BigIntegerField(verbose_name="av号", null=True, blank=True, default=0)
    bvid = models.CharField(verbose_name="bv号", max_length=32, null=True, blank=True, default="#")
    cid = models.BigIntegerField(verbose_name="弹幕id", null=True, blank=True, default=0)
    coin = models.IntegerField(verbose_name="硬币数", null=True, blank=True, default=1)
    ctime = models.BigIntegerField(verbose_name="发布时间", null=True, blank=True, default=0)
    danmu = models.IntegerField(verbose_name="弹幕数", null=True, blank=True, default=0)
    description = models.TextField(verbose_name="简介", null=True, blank=True, default="#")
    favourite = models.IntegerField(verbose_name="收藏数", null=True, blank=True, default=0)
    length = models.IntegerField(verbose_name="长度（秒数）", null=True, blank=True, default=0)
    like = models.IntegerField(verbose_name="点赞数", null=True, blank=True, default=0)
    link = models.CharField(verbose_name="短链接", max_length=255, null=True, blank=True, default="#")
    owner_face = models.CharField(verbose_name="用户头像", max_length=255, null=True, blank=True, default="#")
    owner_mid = models.BigIntegerField(verbose_name="用户uid", null=True, blank=True, default=0)
    owner_name = models.CharField(verbose_name="用户名", max_length=64, null=True, blank=True, default="没有昵称")
    picture = models.CharField(verbose_name="视频封面", max_length=255, null=True, blank=True, default="#")
    pubdate = models.BigIntegerField(verbose_name="审核时间", null=True, blank=True, default=1)
    reason = models.CharField(verbose_name="推荐理由", max_length=64, null=True, blank=True, default="#")
    reply = models.IntegerField(verbose_name="评论数", null=True, blank=True, default=0)
    share = models.IntegerField(verbose_name="分享数", null=True, blank=True, default=0)
    tag_id = models.IntegerField(verbose_name="视频标签id", null=True, blank=True, default=0)
    tag_name = models.CharField(verbose_name="视频标签", max_length=64, null=True, blank=True, default="")
    title = models.TextField(verbose_name="标题", null=True, blank=True, default="标题")
    type_id = models.IntegerField(verbose_name="视频分区id", null=True, blank=True, default=0)
    type_name = models.CharField(verbose_name="视频分区", max_length=64, null=True, blank=True, default="")
    view = models.IntegerField(verbose_name="播放数", null=True, blank=True, default=0)


class PeopleInfo(models.Model):
    archive_view = models.BigIntegerField(verbose_name="视频观看总数", null=True, blank=True, default=0)
    article_view = models.BigIntegerField(verbose_name="专栏观看总数", null=True, blank=True, default=0)
    birthday = models.CharField(verbose_name="生日", max_length=16, null=True, blank=True, default="#")
    count = models.IntegerField(verbose_name="视频总数", null=True, blank=True, default=0)
    face = models.CharField(verbose_name="用户头像", max_length=255, null=True, blank=True, default="#")
    follower = models.IntegerField(verbose_name="粉丝数", null=True, blank=True, default=0)
    following = models.IntegerField(verbose_name="关注数", null=True, blank=True, default=0)
    likes = models.BigIntegerField(verbose_name="获赞总数", null=True, blank=True, default=0)
    mid = models.BigIntegerField(verbose_name="用户uid", null=True, blank=True, default=0)
    name = models.CharField(verbose_name="用户名", max_length=64, null=True, blank=True, default="没有昵称")
    sex = models.CharField(verbose_name="性别", max_length=16, null=True, blank=True, default="保密")
    sign = models.TextField(verbose_name="用户签名", null=True, blank=True, default="-")


class VideoInfo(models.Model):
    aid = models.BigIntegerField(verbose_name="av号", null=True, blank=True, default=0)
    bvid = models.CharField(verbose_name="bv号", max_length=32, null=True, blank=True, default="#")
    cid = models.BigIntegerField(verbose_name="弹幕id", null=True, blank=True, default=0)
    coin = models.IntegerField(verbose_name="硬币数", null=True, blank=True, default=1)
    ctime = models.BigIntegerField(verbose_name="发布时间", null=True, blank=True, default=0)
    danmu = models.IntegerField(verbose_name="弹幕数", null=True, blank=True, default=0)
    description = models.TextField(verbose_name="简介", null=True, blank=True, default="#")
    favourite = models.IntegerField(verbose_name="收藏数", null=True, blank=True, default=0)
    length = models.IntegerField(verbose_name="长度（秒数）", null=True, blank=True, default=0)
    like = models.IntegerField(verbose_name="点赞数", null=True, blank=True, default=0)
    link = models.CharField(verbose_name="短链接", max_length=255, null=True, blank=True, default="#")
    # 不用存放头像，这里的mid与用户表中的mid相关联
    owner_mid = models.BigIntegerField(verbose_name="用户uid", null=True, blank=True, default=0)
    # 不用存放名字
    picture = models.CharField(verbose_name="视频封面", max_length=255, null=True, blank=True, default="#")
    pubdate = models.BigIntegerField(verbose_name="审核时间", null=True, blank=True, default=1)
    # 这里没有reason
    reply = models.IntegerField(verbose_name="评论数", null=True, blank=True, default=0)
    share = models.IntegerField(verbose_name="分享数", null=True, blank=True, default=0)
    tag_id = models.IntegerField(verbose_name="视频标签id", null=True, blank=True, default=0)
    tag_name = models.CharField(verbose_name="视频标签", max_length=64, null=True, blank=True, default="")
    title = models.TextField(verbose_name="标题", null=True, blank=True, default="标题")
    type_id = models.IntegerField(verbose_name="视频分区id", null=True, blank=True, default=0)
    type_name = models.CharField(verbose_name="视频分区", max_length=64, null=True, blank=True, default="")
    view = models.IntegerField(verbose_name="播放数", null=True, blank=True, default=0)
