# coding: utf-8

from django.shortcuts import HttpResponse
import json
import logging
import urllib
from service.commonKey import API


logger = logging.getLogger(__name__)



# 统一返回json数据
def response_json(data):
    return HttpResponse(json.dumps(data), content_type='application/json')

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def tu_ling(req):
    info = req.GET.get('info')
    try:
        url = API + info
        response = getHtml(url)
        dic_json = json.loads(response)
        json_str = {'status': 1, 'msg': dic_json['text']}
    except Exception, exc:
        logger.error(exc, exc_info=True)
        json_str = {'status': 0, 'msg': u'我已经被你撩累了，休息一下下。。。'}
    return response_json(json_str)