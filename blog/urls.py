# coding: utf-8
"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blogSystem import views as blog_views
from blogSystem.account import views as account_views
from blogSystem.common import views as common_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^/?$', blog_views.index, name='index'),
    url(r'^postDetail/?$', blog_views.postDetail, name='postDetail'),

    url(r'^makePost/?$', blog_views.makePost, name='makePost'),

    url(r'^makePostSummit/?$', blog_views.makePostSummit, name='makePostSummit'),

    url(r'^send_mail/?$', blog_views.send_mail, name='send_mail'),

    url(r'^postList/?$', blog_views.postList, name='postList'),
    url(r'^up_down_share_post/?$', blog_views.up_down_share_post, name='up_down_share_post'),
    url(r'^make_post_comment/?$', blog_views.make_post_comment, name='make_post_comment'),
    url(r'^user/(?P<username>\w+)?$', blog_views.user_post, name='user_post'),

    # 帖子详情
    url(r'^category/(?P<category1>\w+)/(?P<post_id>\d+)/?$', blog_views.postDetail, name='category1_post_detail'),
    url(r'^category/(?P<category1>\w+)/(?P<category2>\w+)/(?P<post_id>\d+)/?$', blog_views.postDetail, name='category2_post_detail'),

    # url(r'^category/life/', blog_views.postList, name='categoryLife'),
    # url(r'^category/skills/', blog_views.postList, name='categorySkills'),
    url(r'^welfare/?$', blog_views.postList, name='welfare'),
    url(r'^about/?$', blog_views.postList, name='about'),
    url(r'^leave_message/?$', blog_views.leave_message, name='leave_message'),

    url(r'^accounts/user_logout/?$', account_views.user_logout, name='user_logout'),
    url(r'^accounts/authSetting/?$', account_views.user_auth_setting, name='authSetting'),
    url(r'^accounts/changepwd/?$', account_views.user_change_pwd, name='changepwd'),
    url(r'^accounts/user_login/?$', account_views.user_login, name='user_login'),

    # 帖子分类（一级和二级分类）
    url(r'^category/(?P<category1>\w+)/?$', blog_views.postList, name='category_by1'),
    url(r'^category/(?P<category1>\w+)/(?P<category2>\w+)/?$', blog_views.postList, name='category_by2'),

    url(r'^tuLing/?$', common_views.tu_ling, name='tu_ling'),
    url(r'^make_title_active/?$', common_views.make_title_active, name='make_title_active'),

    url(r'^get_top_three_post/?$', blog_views.get_top_three_post, name='get_top_three_post'),
    url(r'^get_more_message/?$', blog_views.get_more_message, name='get_more_message'),
    url(r'^make_leave_comment_submit/?$', blog_views.make_leave_comment_submit, name='make_leave_comment_submit'),


    url(r'^test/?$', blog_views.test),


]
