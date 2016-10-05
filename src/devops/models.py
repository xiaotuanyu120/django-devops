# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Hosts(models.Model):
    host = models.GenericIPAddressField()
    product = models.CharField(max_length=20)
