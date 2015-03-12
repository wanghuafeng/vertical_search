__author__ = 'wanghuafeng'
# -*- coding: utf-8 -*-
import subprocess
scp_command = 'scp *.py  mdev:~/wanghuafeng/music_spider/'
subprocess.call(scp_command, shell=True)
fab_command = '/usr/local/bin/fab -H mdev --keepalive=10 -- "cd wanghuafeng/music_spider/; python music_fab.py"'
# subprocess.call(fab_command, shell=True)
