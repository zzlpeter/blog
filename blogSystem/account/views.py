# coding: utf-8

from django.contrib.auth import logout, login, authenticate
from django.shortcuts import HttpResponseRedirect, render_to_response, RequestContext
from blogSystem.common.views import response_json
from django.contrib import messages
from blogSystem import models as blog_models
from service.commonFunc import get_user_ip, set_avatar_rendom, send_email
from service.commonKey import IMG_SAVE_ABSOLUTE_PATH
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import os
from django.db import transaction
import re
from service.decorator import is_authenticated
from django.conf import settings
from django.contrib.auth.models import User
import uuid

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

@login_required
def personal_center(req, tmp_name='personal_center.html'):
    return render_to_response(tmp_name, context_instance=RequestContext(req))

# 设置用户昵称
@is_authenticated
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
            name = '%s-%s' % (user.id, name)
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


@login_required
@csrf_exempt
def change_pwd(req):
    old_pwd = req.POST.get('old_pwd')
    new_pwd = req.POST.get('new_pwd')
    confirm_pwd = req.POST.get('confirm_pwd')
    # 检查原密码是否正确
    if not req.user.check_password(old_pwd):
        json_str = {'status': 0, 'msg': u'原密码错误，请检查！'}
        return response_json(json_str)
    # 检查新密码是否符合规则
    if new_pwd != confirm_pwd:
        json_str = {'status': 0, 'msg': u'两次密码输入不一致，请重新输入'}
        return response_json(json_str)
    if not re.match('[a-zA-Z]\w{5,9}', new_pwd):
        json_str = {'status': 0, 'msg': u'密码长度6-10位，以字母开头，只能输入字母、数字、下划线'}
        return response_json(json_str)
    # 保存新密码
    req.user.set_password(new_pwd)
    req.user.save()
    json_str = {'status': 1, 'msg': u'新密码设置成功'}
    return response_json(json_str)


@login_required
@csrf_exempt
def change_other(req):
    user = req.user
    type = req.POST.get('type')
    value = req.POST.get('value')
    try:
        if type == 'name':
            # 检查用户名是否被其他用户占用
            if blog_models.User.objects.exclude(id=user.id).filter(username=value).exists():
                json_str = {'status': 0, 'msg': u'该用户名已被占用，请更换！'}
                return response_json(json_str)
            else:
                user.username = value
                user.save()
                json_str = {'status': 1, 'msg': u'您已成功修改用户名'}
                return response_json(json_str)
        elif type == 'nickName':
            # 检查用户昵称是否被其他用户占用
            if blog_models.UserExtend.objects.exclude(user=user).filter(nickname=value).exists():
                json_str = {'status': 0, 'msg': u'该昵称已被占用，请更换！'}
                return response_json(json_str)
            else:
                user.userextend.nickname = value
                user.userextend.save()
                json_str = {'status': 1, 'msg': u'您已成功修改昵称'}
                return response_json(json_str)
        elif type == 'email':
            if '@' not in value:
                json_str = {'status': 0, 'msg': u'请输入有效邮箱'}
                return response_json(json_str)
            elif value == user.email:
                json_str = {'status': 0, 'msg': u'修改邮箱与原有邮箱一致'}
                return response_json(json_str)
            else:
                # 给新邮箱发确认邮件
                # send_email('update', user, email=value)
                # json_str = {'status': 1, 'msg': u'邮件已发送，请检查邮箱'}
                user.email = value
                user.save()
                json_str = {'status': 1, 'msg': u'修改成功'}
                return response_json(json_str)
        else:
            json_str = {'status': 0, 'msg': u'类型错误，请稍后重试'}
            return response_json(json_str)
    except Exception, exc:
        logger.error(exc, exc_info=True)
        json_str = {'status': 0, 'msg': u'服务器异常，请稍后重试'}
        return response_json(json_str)

# 注册账号
def register_account(req):
    email = req.POST.get('email')
    uname = req.POST.get('uname')
    pwd = req.POST.get('pwd')
    confirm_pwd = req.POST.get('confirm_pwd')
    if pwd != confirm_pwd:
        json_str = {'status': 0, 'msg': u'两次密码输入不一致，请重新输入'}
        return response_json(json_str)
    if not re.match('[a-zA-Z]\w{5,9}', pwd):
        json_str = {'status': 0, 'msg': u'密码长度6-10位，以字母开头，只能输入字母、数字、下划线'}
        return response_json(json_str)
    if User.objects.filter(username=uname).exists():
        json_str = {'status': 0, 'msg': u'该用户名已被注册，请更换'}
        return response_json(json_str)
    if User.objects.filter(email=email).exists():
        json_str = {'status': 0, 'msg': u'该邮箱已被注册，请更换'}
        return response_json(json_str)
    json_str = {'status': 0, 'msg': u'系统异常，请稍后重试'}
    with transaction.atomic():
        user = User.objects.create_user(uname, email, pwd)
        user.is_active = 1
        user.userextend.portrait_id = set_avatar_rendom()
        user.save()
        # send_email('register', user)
        # json_str = {'status': 1, 'msg': u'激活链接已发送到邮箱，请激活'}
        json_str = {'status': 1, 'msg': u'注册成功，请登录'}
    return response_json(json_str)

# 账号激活/修改邮箱
def activate_account(req, uid):
    json_str = {'status': 0, 'msg': u'This link is invalid'}
    try:
        uidObj = blog_models.UUID.objects.get(uuid=uid)
        # 检查该链接是否有效
        if uidObj.is_valid == 0:
            json_str = {'status': 0, 'msg': u'This link is invalid'}
        # 账号激活
        elif uidObj.type == 'register':
            uidObj.user.is_valid = 1
            uidObj.save()
            json_str = {'status': 1, 'msg': u'Your account has been activated, please log in'}
        # 修改邮箱
        elif uidObj.type == 'update':
            uidObj.user.email = uidObj.email
            uidObj.user.save()
            uidObj.save()
            json_str = {'status': 1, 'msg': u'Your email has been updated, thanks'}
    except Exception, exc:
        logger.error(exc, exc_info=True)
        json_str = {'status': 0, 'msg': u'This link is invalid'}
    return response_json(json_str)

# 忘记密码
def forget_pwd(req, tmp_name='forget_pwd.html'):
    return render_to_response(tmp_name, context_instance=RequestContext(req))

# 重新设置密码
def update_forget_pwd(req):
    uname = req.POST.get('uname')
    email = req.POST.get('email')
    pwd = req.POST.get('pwd')
    pwd_again = req.POST.get('pwd_again')

    try:
        user = User.objects.get(username=uname, email=email)
        # 检查新密码是否符合规则
        if pwd != pwd_again:
            json_str = {'status': 0, 'msg': u'两次密码输入不一致，请重新输入'}
            return response_json(json_str)
        if not re.match('[a-zA-Z]\w{5,9}', pwd):
            json_str = {'status': 0, 'msg': u'密码长度6-10位，以字母开头，只能输入字母、数字、下划线'}
            return response_json(json_str)
        # 保存新密码
        user.set_password(pwd)
        user.save()
        json_str = {'status': 1, 'msg': u'新密码设置成功，请登录'}
        return response_json(json_str)
    except Exception, exc:
        logger.error(exc, exc_info=True)
        json_str = {'status': 0, 'msg': u'用户名与邮箱不匹配'}
        return response_json(json_str)




