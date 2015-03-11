__author__ = 'huafeng'
#coding:utf-8
import subprocess
scp_command = 'scp *.py  mdev:~/wanghuafeng/movie_spider/'
subprocess.call(scp_command, shell=True)
fab_command = '/usr/local/bin/fab -H mdev --keepalive=10 -- "cd wanghuafeng/movie_spider/; python movie_fab.py"'
subprocess.call(fab_command, shell=True)

