# coding: utf-8

from django import template

register = template.Library()


# django model func template parameter
@register.simple_tag
def get_post_related_num(func, params):
    return func.get_post_related_num(params)