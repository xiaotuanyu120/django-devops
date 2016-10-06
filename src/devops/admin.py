# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Host

class HostAdmin(admin.ModelAdmin):
    list_display = ('host', 'hostname', 'PIC', 'created', 'updated')

# admin.site.register(Hosts, HostAdmin)
admin.site.register(Host, HostAdmin)
