# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
# from django.contrib.auth.forms import PasswordChangeForm
from .models import Host, Brand


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['host', 'brand', 'service_type']


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand']


class PasswordChangeFormCustom(forms.Form):
    oldpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    newpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    repeatnewpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_repeatnewpassword(self):
        newpassword = self.cleaned_data.get('newpassword')
        repeatnewpassword = self.cleaned_data.get('repeatnewpassword')
        if not newpassword == repeatnewpassword:
            raise forms.ValidationError("Password is not same!")
        return repeatnewpassword
