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
    if(request.GET.get("run")):
        cmd = request.GET.get("cmd")
        host = request.GET.get("host")

        runner = AnsibleRunner()
        runner.init_inventory(host_list='localhost')
        runner.init_play(hosts='localhost', module='shell', args='ls')
        result = runner.run_it()

    return render(request, "devops/dashboard.html", context)
