# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='login_user'),
    # url(r'^logged/$', views.logged, name='logged_user'),
    url(r'^record/$', views.record, name='record'),
    url(r'^profile/$', views.profile, name='user_profile'),
    url(r'^run/$', views.execute, name='run'),
    url(r'^ansible_hosts/$', views.ansible_hosts, name='ansible_hosts'),
]
