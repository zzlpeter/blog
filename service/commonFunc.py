# coding: utf-8

import logging
from blogSystem.models import Images, Post, PostComment, UUID
import random
from service.commonKey import COMMENT_SCORE, POST_SCORE
import uuid
from service.emails import Email


logger = logging.getLogger(__name__)


# 获取用户IP
def get_user_ip(req):
    try:
        if req.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = req.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = req.META['REMOTE_ADDR']
    except Exception, exc:
        logger.error(exc, exc_info=True)
        ip = ''
    return ip

# 随机设置用户头像
def set_avatar_rendom():
    id_list = Images.objects.filter(img_category__name='portrait').values_list('id')
    count = len(id_list)
    rand = random.randint(0, count - 1)
    return int(id_list[rand][0])

# 获取用户等级
def get_user_level(uid):
    post_count = Post.objects.filter(author_id=uid).count()
    comment_count = PostComment.objects.filter(poster_id=uid).count()
    score = post_count * POST_SCORE + comment_count * COMMENT_SCORE
    if score in range(0, 1):
        level = {
            'star': 0,
            'half': 0,
            'no_star': 5
        }
    elif score in range(1, 10):
        level = {
            'star': 1,
            'half': 0,
            'no_star': 4
        }
    elif score in range(10, 20):
        level = {
            'star': 1,
            'half': 1,
            'no_star': 3
        }
    elif score in range(20, 30):
        level = {
            'star': 2,
            'half': 1,
            'no_star': 2
        }
    elif score in range(30, 40):
        level = {
            'star': 3,
            'half': 0,
            'no_star': 2
        }
    else:
        level = {
            'star': 5,
            'half': 0,
            'no_star': 0
        }
    return level

# 生成UUID1
def uid1():
    return uuid.uuid1()

# 发送邮件
def send_email(te, user, email=None):
    # 首先插入UUID表记录
    uid = UUID()
    tmp_uuid = uid1()
    uid.uuid = tmp_uuid
    uid.type = te
    uid.user = user
    uid.is_valid = 1
    if email:
        uid.email = email
    uid.save()
    if te == 'register':
        mail_content = '''
                            <html>
                                <h5>尊敬的用户您好</h5>
                                <h5>欢迎注册伊诺的博客</h5>
                                <h5>您的博客账号已开通，请点击以下链接激活账号：</h5>
                                <h5><a href='http://zzl.papasecret.com/accounts/activate_account/%s'>点我激活</a></h5>
                            </html>
                        '''%tmp_uuid
        tmp_email = user.email
    else:
        mail_content = '''
                            <html>
                                <h5>尊敬的用户您好</h5>
                                <h5>欢迎注册伊诺的博客</h5>
                                <h5>请点击以下链接更新邮箱信息：</h5>
                                <h5><a href='http://zzl.papasecret.com/accounts/activate_account/%s'>点我更新</a></h5>
                            </html>
                        ''' % tmp_uuid
        tmp_email = email
    em = Email(tmp_email, mail_content)
    em.send()