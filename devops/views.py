# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from subprocess import check_output
from django.contrib.auth.models import User
from .models import Host, Brand
from .forms import PasswordChangeFormCustom
import sys
import json



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
    return render_to_response('devops/login.html',
                        context_instance=RequestContext(request))


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
    # get information of logined user
    user_login_name = request.user.username
    firstname = request.user.first_name
    lastname = request.user.last_name
    email = request.user.email
    groups = request.user.groups

    # form for password change
    form = PasswordChangeFormCustom(request.POST or None)
    context = {
        'user_login_name': user_login_name,
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'groups': groups,
        'form': form,
    }

    # password changing function
    if request.POST:
        if form.is_valid():
            new = request.POST.get("newpassword")
            u = User.objects.get(username=request.user.username)
            u.set_password(new)
            u.save()
            # replace form with a password changed message
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


def dashboard(request):
    if not request.user.is_authenticated():
        return render(request, "devops/login.html")

    # username for main.html
    user_login_name = request.user.username

    # initial hosts and brands for selection form
    hosts = Host.objects.all()
    brands = ["请选择产品品牌"]
    for brand in Brand.objects.all():
        if not brand in brands:
            brands.append(brand)
    context = {
        'user_login_name': user_login_name,
        "hosts": hosts,
        "brands": brands,
    }

    # function for command running
    if request.POST:
        if(request.POST.get("run")):
            # strip去两边空格，split+join去除中间重复空格，然后split转换字符串为list
            cmd = ' '.join(request.POST.get('cmd').strip().split()).split()
            print cmd
            try:
                stdout = check_output(cmd)
            except:
                stdout = "CMD:" + str(cmd) + " CMD error:" + str(sys.exc_info())
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


@csrf_protect
@login_required
def form_interaction(request):
    if request.POST:
        selected_brand = request.POST.get('selbrand')
        host_list = []
        filtered_host = Host.objects.filter(brand__brand=selected_brand)
        for brand_item in filtered_host:
            if host_list.count(brand_item) == 0:
                brand_item = str(brand_item)
                host_list.append(brand_item)
        host = json.dumps(host_list)
        return HttpResponse(host, content_type="application/json")
