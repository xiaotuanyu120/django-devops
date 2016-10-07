# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,render_to_response,redirect
from .models import Host
from .ansible_api_2 import AnsibleRunner

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import *
from django.views.decorators.csrf import csrf_protect
import os, sys
from subprocess import Popen, PIPE, check_output



def index(request):
    if(request.GET.get("signin")):
        print(request.GET.get("username"))
    return render(request, "devops/index.html")


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
    return render(request, 'devops/logged.html')


def dashboard(request):
    hosts = Host.objects.all()
    context = {
        "hosts": hosts,
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
            print stdout
            context = {
                "hosts": hosts,
                "stdout": stdout,
            }

        # runner = AnsibleRunner()
        # runner.init_inventory(host_list='localhost')
        # runner.init_play(hosts='localhost', module='shell', args='ls')
        # result = runner.run_it()

    return render(request, "devops/dashboard.html", context)
