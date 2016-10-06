# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Host
from .forms import HostForm


class HostAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'hostname', 'PIC', 'created', 'updated')
    form = HostForm

# admin.site.register(Hosts, HostAdmin)
admin.site.register(Host, HostAdmin)
