# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""classmate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('devops.urls')),
    # url('^', include('django.contrib.auth.urls')),
    # url('^change-password/$', auth_views.password_change, {'template_name': 'devops/change-password.html'}),
]
