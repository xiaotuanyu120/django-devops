# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Host, Brand
from .forms import HostForm, BrandForm


class HostAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'hosttag', 'brand', 'service_type', 'created', 'updated')
    form = HostForm


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand','created', 'updated')
    form = BrandForm

# admin.site.register(Hosts, HostAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Brand, BrandAdmin)
