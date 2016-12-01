# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import json
from datetime import datetime
from subprocess import check_output, Popen

from django.http import *
from django.shortcuts import render,render_to_response,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone

from .models import Host, Brand, Record, BackupRecord
from .forms import PasswordChangeFormCustom
from .hosts_parser import HostsParser


def index(request):
    return render(request, "devops/login.html")


def home(request):
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
                return HttpResponseRedirect('/home/')
    return render_to_response('devops/login.html', context_instance=RequestContext(request))


@login_required
def logout_user(request):
    logout(request)
    return redirect('login_user')


@login_required
def profile(request):
    firstname = request.user.first_name
    lastname = request.user.last_name
    email = request.user.email
    groups = request.user.groups

    form = PasswordChangeFormCustom(request.POST or None)
    context = {
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
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'groups': groups,
                'changed_password': changed_password,
            }
    return render(request, 'devops/profile.html', context)


def _record(record_list):
    record = Record(user=record_list['user'],
                    brand=record_list['brand'],
                    from_ip=record_list['from_ip'],
                    cmd=record_list['cmd'],
                    action=record_list['action'])
    record.save()


@login_required
def record(request):
    filter_fields = {f.verbose_name: f.name for f in Record._meta.get_fields() \
            if f.verbose_name not in ['ID', u'命令', u'动作']}
    filter_str = str(datetime.now()).split()[0]
    filter_field = 'action_time'
    if request.POST.get('filter_str') and request.POST.get('filter_field'):
        filter_str = request.POST.get('filter_str')
        filter_field = filter_fields[request.POST.get('filter_field')]
    filter_field_contains = '%s__contains' % filter_field
    my_filter = {}
    my_filter[filter_field_contains] = filter_str
    try:
        records = Record.objects.filter(**my_filter).order_by('-action_time', 'user').values()
    except:
        records = Record.objects.filter(action_time__contains=filter_str).order_by('-action_time', 'user').values()

    context = {
        'records': records,
        'filter_fields': filter_fields
    }
    return render(request,"devops/record.html", context)


def _execute(cmd):
    '''
    execute cmd
    '''
    result = {}
    try:
        stdout = check_output(cmd)
        stderr = ''
    except:
        stdout = ''
        stderr = str(sys.exc_info())
    result['stdout'] = stdout
    result['stderr'] = stderr
    return result


def execute(request):
    if request.method == 'POST' and request.is_ajax():
        ansible_dir = settings.ANSIBLE_DIR
        ansible_playbook_path = settings.ANSIBLE_PLAYBOOK_PATH
        inventory = "%s/%s" % (ansible_dir, 'hosts')
        yml_file = "%s/%s" % (ansible_dir, 'main.yml')
        selbrand = request.POST['selbrand']
        sertype = request.POST['sertype']
        args = "host=%s_%s" % (Brand.objects.filter(name=selbrand).values()[0]["brand"], sertype)
        cmd = [ansible_playbook_path, '-i', inventory, yml_file, "-e", args]
        cmd_exec = _execute(cmd)
        stdout = cmd_exec['stdout']
        stderr = cmd_exec['stderr']
        print stdout
        if not stdout:
            stdout = stderr
        else:
            try:
                record_list = {
                    'user': request.POST['user'],
                    'brand': selbrand,
                    'from_ip': user_ip(request),
                    'cmd': ' '.join(cmd),
                    'action': 'TR',
                }
            except:
                print sys.exc_info()[0]
            _record(record_list)

        try:
            stdout = str(stdout)
            stdout = stdout.splitlines()
        except:
            e = sys.exc_info()[0]
            print "error" + str(e)

        return HttpResponse(json.dumps(stdout), content_type = "application/json")
    return HttpResponseNotFound('<h1>Page not found</h1>')


def user_ip(input):
    try:
        return input.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
    except:
        return input.META.get('REMOTE_ADDR')


def check_permission(user):
    allowed_user = settings.DASHBOARD_USERS
    if user.username not in allowed_user:
        return False
    else:
        return True


@user_passes_test(check_permission)
@login_required
def dashboard(request):
    hosts = Host.objects.all()
    brands = Brand.objects.all()
    context = {
        "hosts": hosts,
        "brands": brands,
    }
    return render(request, "devops/dashboard.html", context)


@login_required
def ansible_hosts(request):
    hosts_file = "%s/%s" % (settings.ANSIBLE_DIR, 'hosts')
    hosts = HostsParser()
    hosts_list = hosts.parser(hosts_file)

    top_group = {}
    sub_group = {}
    for li in hosts_list:
        if type(hosts_list[li]) is dict:
            top_group[li] = hosts_list[li]
        elif type(hosts_list[li]) is list:
            sub_group[li] = hosts_list[li]

    context = {
        "top_group": top_group,
        "sub_group": sub_group
    }
    return render(request, "devops/ansible_hosts.html", context)


@csrf_exempt
def bbs_backup_api(request):
    if request.POST:
        try:
            record = BackupRecord(brand_bbs = request.POST["brand_bbs"],
                                  host_ip = request.POST["host_ip"],
                                  backup_result = request.POST["backup_result"],)
            record.save()
        except:
            print sys.exc_info()
            context = {"result": "FAILED"}
            return HttpResponse(json.dumps(context), content_type = "application/json")
        context = {"result": "SUCCESSED"}
        return HttpResponse(json.dumps(context), content_type = "application/json")
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required
def bbs_backup_record(request):
    records = BackupRecord.objects.all().values()
    context = {"records": records}
    return render(request,"devops/bbs_backup_record.html", context)
