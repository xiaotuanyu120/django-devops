# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render


def index(request):

    if(request.GET.get("signin")):
        print(request.GET.get("username"))
    return render(request, "devops/index.html")

def dashboard(request):
    if(request.GET.get("run")):
        print(request.GET.get("cmd"))
        print(request.GET.get("host"))
    return render(request, "devops/dashboard.html")
