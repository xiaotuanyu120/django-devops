# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Host
from .ansible_api_2 import AnsibleRunner


def index(request):

    if(request.GET.get("signin")):
        print(request.GET.get("username"))
    return render(request, "devops/index.html")

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
