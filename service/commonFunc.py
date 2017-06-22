# coding: utf-8

import logging


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