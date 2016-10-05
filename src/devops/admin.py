# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Hosts

class HostAdmin(admin.ModelAdmin):
    list_display = ('host', 'product')

admin.site.register(Hosts, HostAdmin)
