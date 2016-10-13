# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logged/$', views.logged, name='logged_user'),
    url(r'^profile/$', views.profile, name='profile')
]
