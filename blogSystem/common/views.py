# coding: utf-8

from django.shortcuts import HttpResponse
import json
import logging
import urllib
from service.commonKey import API
from datetime import datetime


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
    time = datetime.now().strftime('%H:%M:%S')
    try:
        url = API + info.encode('utf-8')
        response = getHtml(url)
        dic_json = json.loads(response)
        json_str = {'status': 1, 'msg': dic_json['text'], 'time': time}
    except Exception, exc:
        logger.error(exc, exc_info=True)
        json_str = {'status': 0, 'msg': u'我已经被你撩累了，休息一下下。。。', 'time': time}
    return response_json(json_str)

def make_title_active(req):
    path = req.META['HTTP_REFERER']
    if 'life' in path:
        json_str = {'active': 'life'}
    elif 'skills' in path:
        json_str = {'active': 'skills'}
    elif 'welfare' in path:
        json_str = {'active': 'welfare'}
    elif 'about' in path:
        json_str = {'active': 'about'}
    elif 'leave' in path:
        json_str = {'active': 'leave'}
    else:
        json_str = {'active': 'index'}
    return response_json(json_str)