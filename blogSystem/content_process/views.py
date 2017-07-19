# coding: utf-8

from django.conf import settings


def is_can_register(req):
    content = {
        'can_register': settings.CAN_REGISTER
    }
    return content