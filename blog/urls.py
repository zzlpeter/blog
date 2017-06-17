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

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^/?$', blog_views.index, name='index'),
    url(r'^postDetail/?$', blog_views.postDetail, name='postDetail'),

    url(r'^makePost/?$', blog_views.makePost, name='makePost'),

    url(r'^makePostSummit/?$', blog_views.makePostSummit, name='makePostSummit'),

    url(r'^send_mail/?$', blog_views.send_mail, name='send_mail'),

    url(r'^postList/?$', blog_views.postList, name='postList'),

    url(r'^category/(?P<category1>\w+)/(?P<post_id>\d+)/?$', blog_views.postDetail, name='category1_post_detail'),
    url(r'^category/(?P<category1>\w+)/(?P<category2>\w+)/(?P<post_id>\d+)/?$', blog_views.postDetail, name='category2_post_detail'),

    # url(r'^category/life/', blog_views.postList, name='categoryLife'),
    # url(r'^category/skills/', blog_views.postList, name='categorySkills'),
    url(r'^welfare/?$', blog_views.postList, name='welfare'),
    url(r'^about/?$', blog_views.postList, name='about'),

    url(r'^accounts/user_logout/?$', blog_views.user_logout, name='user_logout'),
    url(r'^accounts/authSetting/?$', blog_views.postList, name='authSetting'),
    url(r'^accounts/changepwd/?$', blog_views.postList, name='changepwd'),
    url(r'^accounts/user_login/?$', blog_views.user_login, name='user_login'),

    url(r'^category/(?P<category1>\w+)/?$', blog_views.postList, name='category_by1'),
    url(r'^category/(?P<category1>\w+)/(?P<category2>\w+)/?$', blog_views.postList, name='category_by2'),
]
