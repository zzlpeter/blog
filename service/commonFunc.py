# coding: utf-8

import logging
from blogSystem.models import Images
import random


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
    return id_list[rand]