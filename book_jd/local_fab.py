__author__ = 'wanghuafeng'
# -*- coding: utf-8 -*-
import subprocess
spider_name = 'book'
scp_command = 'scp *.py  mdev:~/wanghuafeng/%s_spider/' % spider_name
subprocess.call(scp_command, shell=True)
fab_command = '/usr/local/bin/fab -H mdev --keepalive=10 -- "cd wanghuafeng/%s_spider/; python %s_fab.py"' % (spider_name, spider_name)
subprocess.call(fab_command, shell=True)
