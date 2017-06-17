# coding: utf-8

from django.shortcuts import HttpResponse
import json
import logging

logger = logging.getLogger(__name__)



# 统一返回json数据
def response_json(data):
    return HttpResponse(json.dumps(data), content_type='application/json')