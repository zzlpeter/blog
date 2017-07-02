# coding: utf-8

from django.contrib.auth import logout, login, authenticate
from django.shortcuts import HttpResponseRedirect, render_to_response, RequestContext
from blogSystem.common.views import response_json
from django.contrib import messages
from blogSystem import models as blog_models
from service.commonFunc import get_user_ip



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