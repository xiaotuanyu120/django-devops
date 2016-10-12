# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,render_to_response,redirect
from .models import Host, Brand
from .ansible_api_2 import AnsibleRunner

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import *
from django.views.decorators.csrf import csrf_protect
import os, sys
from subprocess import check_output
from django.contrib.auth.models import User
from .forms import PasswordChangeFormCustom


def index(request):
    user_login_name = None
    if request.user.is_authenticated():
        user_login_name = request.user.username
    context = {
        'user_login_name': user_login_name
    }
    return render(request, "devops/index.html", context)


@csrf_protect
def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/logged/')
    return render_to_response('devops/login.html', context_instance=RequestContext(request))


def logged(request):
    user_login_name = None
    if request.user.is_authenticated():
        user_login_name = request.user.username
    context = {
        'user_login_name': user_login_name
    }
    return render(request, 'devops/logged.html', context)


# @login_required
def profile(request):
    if not request.user.is_authenticated():
        return render(request, "devops/login.html")
    user_login_name = request.user.username
    firstname = request.user.first_name
    lastname = request.user.last_name
    email = request.user.email
    groups = request.user.groups

    form = PasswordChangeFormCustom(request.POST or None)
    context = {
        'user_login_name': user_login_name,
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'groups': groups,
        'form': form,
    }
    if request.POST:
        if form.is_valid():
            old = request.POST.get("oldpassword")
            new = request.POST.get("newpassword")
            new2 = request.POST.get("repeatnewpassword")
            u = User.objects.get(username=request.user.username)
            u.set_password(new)
            u.save()

            changed_password = "your password have been changed!"
            context = {
                'user_login_name': user_login_name,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'groups': groups,
                'changed_password': changed_password,
            }
    return render(request, 'devops/profile.html', context)


#
# 只有登录过的用户才能访问dashboard
#
@login_required()
def dashboard(request):
    user_login_name = request.user.username
    hosts = Host.objects.all()
    brands = Brand.objects.all()
    context = {
        'user_login_name': user_login_name,
        "hosts": hosts,
        "brands": brands,
    }
    if request.POST:
        if(request.POST.get("run")):
            # strip去两边空格，split+join去除中间重复空格，然后split转换字符串为list
            cmd = ' '.join(request.POST.get('cmd').strip().split()).split()
            print cmd
            try:
                stdout = check_output(cmd)
            except:
                stdout = "CMD :" + str(cmd) + " CMD error: " + str(sys.exc_info())
            context = {
                'user_login_name': user_login_name,
                "hosts": hosts,
                "stdout": stdout,
                "brands": brands,
            }

        # runner = AnsibleRunner()
        # runner.init_inventory(host_list='localhost')
        # runner.init_play(hosts='localhost', module='shell', args='ls')
        # result = runner.run_it()

    return render(request, "devops/dashboard.html", context)
