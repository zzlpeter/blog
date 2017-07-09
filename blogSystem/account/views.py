# coding: utf-8

from django.contrib.auth import logout, login, authenticate
from django.shortcuts import HttpResponseRedirect, render_to_response, RequestContext
from blogSystem.common.views import response_json
from django.contrib import messages
from blogSystem import models as blog_models
from service.commonFunc import get_user_ip
from service.commonKey import IMG_SAVE_ABSOLUTE_PATH
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import os
from django.db import transaction

import logging

logger = logging.getLogger(__name__)



# 用户登出
def user_logout(req):
    logout(req)
    messages.add_message(req, messages.INFO, u'您已成功退出！')
    return HttpResponseRedirect('/')

# 用户登录
def user_login(req):
    username = req.POST.get('username')
    password = req.POST.get('password')
    remember = req.POST.get('remember')
    if req.user.is_authenticated():
        json_str = {'status': 0, 'msg': u'您已登录，不可重复登录！'}
        return response_json(json_str)
    user = authenticate(username=username, password=password)
    if user is not None:
        if not user.is_active:
            json_str = {'status': 0, 'msg': u'您的账号处于未激活状态，请激活！'}
        else:
            login(req, user)
            ip = get_user_ip(req)
            blog_models.UserExtend.objects.filter(user=user).update(login_ip=ip)
            json_str = {'status': 1, 'msg': u'您已成功登陆！'}
    else:
        json_str = {'status': 0, 'msg': u'用户名与密码不匹配，请检查！'}
    return response_json(json_str)

# 用户权限设置
def user_auth_setting(req):
    pass

# 用户改密码
def user_change_pwd(req):
    pass

def personal_center(req, tmp_name='personal_center.html'):
    return render_to_response(tmp_name, context_instance=RequestContext(req))

# 设置用户昵称
@login_required
def set_nickname(req):
    user = req.user
    nickname = req.GET.get('nickname')
    if not nickname.strip():
        json_str = {'status': 0, 'msg': u'昵称不允许为空'}
        return response_json(json_str)
    blog_models.UserExtend.objects.filter(user=user).update(nickname=nickname)
    json_str = {'status': 1, 'msg': u'昵称设置成功'}
    return response_json(json_str)

# 上传头像
@login_required
@csrf_exempt
def upload_avatar(req):
    user = req.user
    avatar = req.FILES.get('avatar')
    try:
        # 检查用户是否选择文件
        if not avatar:
            json_str = {'status': 0, 'msg': u'请选择需要上传的图片'}
            return response_json(json_str)
        # 检查文件大小及格式
        name = avatar.name
        size = avatar.size
        foramt = avatar.content_type.split('/')[1]
        if foramt not in ('jpg', 'png', 'jpeg'):
            json_str = {'status': 0, 'msg': u'请选择JPG/PNG/JPEG格式的图片'}
            return response_json(json_str)
        if size > 2 * 1024 * 1024:
            json_str = {'status': 0, 'msg': u'请上传2M以内的图片'}
            return response_json(json_str)

        # 图片插入记录及修改用户头像走原子操作
        with transaction.atomic():
            path = os.path.join(IMG_SAVE_ABSOLUTE_PATH, name)
            save = open(path, 'wb')
            save.write(avatar.read())
            img = blog_models.Images.objects.create(
                    src=name,
                    img_category_id=blog_models.ImagesCategory.objects.get(name='other').id
                )
            blog_models.UserExtend.objects.filter(user=user).update(portrait_id=img.id)
        json_str = {
            'status': 1,
            'msg': u'头像上传成功',
            'img': '/static/images/other/%s' % user.userextend.portrait.src
        }
        return response_json(json_str)
    except Exception, exc:
        logger.error(exc, exc_info=True)
        json_str = {'status': 0, 'msg': u'图片上传异常，请检查图片格式'}
        return response_json(json_str)



