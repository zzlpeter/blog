# coding: utf-8

from django.shortcuts import HttpResponse
import json


def is_authenticated(func=None):
    def check(req):
        if req.user.is_authenticated():
            pass
        else:
            json_str = {'status': 0, 'msg': u'登录之后才可操作'}
            return HttpResponse(json.dumps(json_str), content_type='application/json')
    return check