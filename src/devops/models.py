# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# class Staff(models.Model):
#     staff = models.CharField(max_length=20)
#     fullname = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.staff
#
#     def __unicode__(self):
#         return self.staff


class Brand(models.Model):
    brand = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.brand

    def __unicode__(self):
        return self.brand


class Host(models.Model):
    service_type_list = {
        ('web', "web"),
        ('ser', "service"),
    }
    host = models.GenericIPAddressField()
    hosttag = models.CharField(max_length=20)
    brand = models.ForeignKey(Brand, null=True)
    service_type = models.CharField(max_length=3, choices=service_type_list, default='web')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.host

    def __unicode__(self):
        return self.host

    def save(self, *args, **kwargs):
        self.hosttag = self.host + '_' + self.brand.brand + '_' + self.service_type
        print self.hosttag
        super(Host, self).save(*args, **kwargs)
