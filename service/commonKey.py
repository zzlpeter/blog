# coding: utf-8

import random

# 博客大类型分类
CATEGORY_DICT = {
    'skills': u'技术杂谈',
    'welfare': u'福利专区',
    'life': u'生活笔记'
}


# 图灵机器人接口
KEY_LIST = [
    '8b005db5f57556fb96dfd98fbccfab84',
    'cb82e1cce48542e18e882ddc7b5c42f5'
]
API = 'http://www.tuling123.com/openapi/api?key=' + KEY_LIST[random.choice(range(len(KEY_LIST)))] + '&info='


# 帖子10分、评论5分
POST_SCORE = 10
COMMENT_SCORE = 5


# 图片保存路径(绝对路径)
IMG_SAVE_ABSOLUTE_PATH = '/root/zzl/blog/static/images/other'