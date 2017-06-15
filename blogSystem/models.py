# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'blog_user_extend'



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
    title = models.CharField(max_length=100)
    author = models.ForeignKey(UserExtend)
    summary = models.CharField(max_length=500)
    img = models.ForeignKey(Images)
    post_time = models.DateTimeField(auto_now=True)
    content = models.TextField()
    is_valid = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog_post'


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

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'blog_message_leave'
