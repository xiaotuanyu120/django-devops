# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=20, null=True, default="default_name")
    brand = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


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


class Record(models.Model):
    action_list = {
        ('TR', 'tomcat_restart'),
    }
    user = models.CharField(max_length=20, verbose_name="用户")
    brand = models.CharField(max_length=20, verbose_name="品牌")
    from_ip = models.GenericIPAddressField(verbose_name="IP")
    cmd = models.CharField(max_length=50, verbose_name="命令")
    action = models.CharField(max_length=5, choices=action_list, verbose_name="动作")
    action_time = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="执行时间")


class BackupRecord(models.Model):
    brand_bbs = models.CharField(max_length=20, verbose_name="论坛品牌")
    host_ip = models.GenericIPAddressField(verbose_name="论坛ip")
    backup_result = models.CharField(max_length=10, verbose_name="备份结果")
    backup_date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="备份时间")
