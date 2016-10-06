# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

from .models import Host

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = [ 'PIC', 'host', 'hostname']
