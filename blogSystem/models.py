# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

# Create your models here.

class test(models.Model):
    file_name = models.CharField(max_length=100)
    receivers = models.CharField(max_length=200)

    class Meta:
        db_table = 'test'




class ImagesCategory(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'blog_images_category'


class Images(models.Model):
    id = models.AutoField(primary_key=True)
    upload_time = models.DateTimeField(auto_now=True)
    src = models.CharField(max_length=100)
    img_category = models.ForeignKey(ImagesCategory)

    def __str__(self):
        return self.img_category

    class Meta:
        db_table = 'blog_images'


class UserExtend(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    portrait = models.ForeignKey(Images)
    login_ip = models.CharField(max_length=100, blank=True, null=True)
    nickname = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user

    def is_pay_attention_to_user(self, uid):
        if UserAttention.objects.filter(guan_zhu=self.id, bei_guan_zhu=uid).exists():
            return 'yes'
        else:
            return 'no'

    class Meta:
        db_table = 'blog_user_extend'

    @receiver(post_save, sender=User)
    def create_user_user_extend(sender, instance, created, **kwargs):
        if created:
            UserExtend.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_user_extend(sender, instance, **kwargs):
        instance.userextend.save()



class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now=True)
    level = models.SmallIntegerField()
    parent_level = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'blog_category'


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(UserExtend)
    summary = models.CharField(max_length=500, blank=True, null=True)
    img = models.ForeignKey(Images)
    post_time = models.DateTimeField(auto_now=True)
    content = models.TextField()
    category = models.ForeignKey(Category)
    is_valid = models.SmallIntegerField(default=1)
    scan = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog_post'

    # 获取该帖子作者一共发帖数量
    def post_count_belong_this_user(self):
        try:
            count = Post.objects.filter(author_id=self.author_id).count()
        except Exception, exc:
            logger.error(exc, exc_info=True)
            count = 1
        return count

    # 获取该帖子路径
    def post_detail_path(self):
        level2 = Category.objects.get(pk=self.category_id).name
        level1 = Category.objects.get(pk=self.category.parent_level).name
        return '/category/%s/%s/%s' % (level1, level2, self.id)

    # 获取该帖子喜欢、不喜欢、阅读、分享数量
    def get_post_related_num(self, type):
        if type in ('up', 'down'):
            return ThumbUpDown.objects.filter(thumb_type=type, post_id=self.id).count()
        elif type == 'share':
            return PostShare.objects.filter(post_id=self.id).count()
        elif type == 'scan':
            return self.scan

    # 获取评论数量
    def get_comment_count(self):
        return PostComment.objects.filter(post_id=self.id).count()

    # 获取帖子所属分类
    # 若有二级分类，则忽略一级分类
    def get_post_cat(self):
        try:
            return Category.objects.get(pk=self.category_id).name
        except Exception, exc:
            return Category.objects.get(pk=self.category.parent_level).name



class ThumbUpDown(models.Model):
    thumb_choice = (
        ('up', u'支持'),
        ('down', u'反对')
    )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserExtend)
    thumb_time = models.DateTimeField(auto_now=True)
    thumb_type = models.CharField(max_length=5, choices=thumb_choice)
    post = models.ForeignKey(Post)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'blog_thumb_up_down'


class PostShare(models.Model):
    dest_choice = (
        ('qzone', u'QQ空间'),
        ('tsina', u'新浪微博'),
        ('tqq', u'腾讯微博'),
        ('renren', u'人人'),
        ('wechat', u'微信')
    )
    id = models.AutoField(primary_key=True)
    share_time = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post)
    destination = models.CharField(max_length=10, choices=dest_choice)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'blog_post_share'


class PostComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment_time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=1000)
    post = models.ForeignKey(Post)
    poster = models.ForeignKey(UserExtend)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'blog_post_comment'


class MessageLeave(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=1000)
    leave_time = models.DateTimeField(auto_now=True)
    leaver = models.ForeignKey(UserExtend)
    level = models.SmallIntegerField()
    parent_id = models.IntegerField(default=0)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'blog_message_leave'


class UserAttention(models.Model):
    id = models.AutoField(primary_key=True)
    guan_zhu = models.IntegerField()
    bei_guan_zhu = models.IntegerField()
    email_notice = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'blog_user_attention'


class UserMessageCenter(models.Model):
    id = models.AutoField(primary_key=True)
    reader = models.ForeignKey(UserExtend)
    message = models.CharField(max_length=1000)
    msg_time = models.DateTimeField(auto_now=True)
    is_read = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'blog_user_message_center'
