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

    url(r'^index/?$', blog_views.index, name='index'),
    url(r'^no_sidebar/?$', blog_views.no_sidebar, name='no_sidebar'),

    url(r'^showdown/?$', blog_views.showdown, name='showdown'),

    url(r'^send_mail/', blog_views.send_mail, name='send_mail'),

    url(r'^list1/', blog_views.list1, name='list1'),
]
