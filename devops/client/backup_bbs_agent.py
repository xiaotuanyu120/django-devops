# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib
import urllib2

# settings
url = 'http://69.172.81.6:999/bbs_backup_api/'
headers = {'User-Agent': 'Magic Browser'}
backup_log_file = "bbs_backup.log"


def record_backup(input, url, headers):
    brand_bbs, host_ip, backup_result = input.split()
    data = urllib.urlencode({"brand_bbs":brand_bbs, "host_ip":host_ip, "backup_result":backup_result})
    req = urllib2.Request(url, data=data, headers=headers)
    f = urllib2.urlopen(req)
    return f.read()


if __name__ == "__main__":
    with open(backup_log_file, 'r') as f:
        for line in f:
            if len(line.split()) is 3:
                result = record_backup(line, url, headers)
                print "%s: backup is %s" % (line.split()[0], result)
            else:
                print "please check the backup log file!"
