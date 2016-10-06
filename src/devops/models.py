# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Host(models.Model):
    host = models.GenericIPAddressField()
    hostname = models.CharField(max_length=20)
    PIC = models.CharField(max_length=20, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.host

    def __unicode__(self):
        return self.host
