# coding: utf-8

from django.shortcuts import HttpResponse, Http404
import json
from django.conf import settings


def is_authenticated(func=None):
    '''
    用户是否登录装饰器，区别与login_required，返回json
    :param func: 
    :return: 
    '''
    def check(req, **kwargs):
        if req.user.is_authenticated():
            return func(req, **kwargs)
        else:
            json_str = {'status': 0, 'msg': u'登录之后才可操作'}
            return HttpResponse(json.dumps(json_str), content_type='application/json')
    return check


def is_can_register(func=None):
    '''
    是否可以注册装饰器
    :param func: 
    :return: 
    '''
    def dec(req, **kwargs):
        if settings.CAN_REGISTER:
            return func(req, **kwargs)
        else:
            return Http404
    return dec