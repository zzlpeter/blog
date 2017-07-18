# coding: utf-8

import blogSystem.models as blog_models
from django.shortcuts import render_to_response, RequestContext
import json
from django.db.models import Q
import time
from itertools import chain



def search(req, tmp_name='postList.html'):
    start = time.time()
    query = req.GET.get('q', '')
    qs = query.split(' ')

    breads = [
        {'location': u'首页', 'href': '/'},
        {'location': query}
    ]
    s_list = []
    for q in qs:
        post = blog_models.Post.objects.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(content__icontains=q))
        s_list.append(post)
    posts = chain.from_iterable(s_list)
    end = time.time()
    dic = {
        'breads': breads,
        'posts': posts,
        'q': query,
        'time': str(round((end - start), 3)) + 's'
    }
    return render_to_response(tmp_name, dic, context_instance=RequestContext(req))
