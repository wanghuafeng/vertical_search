__author__ = 'wanghuafeng'
#coding:utf-8
import subprocess
import os
import codecs

def mdev_fab():
    log_obj = codecs.open('music.log', mode='ab')
    s3_remote_path = '/home/ferrero/wanghuafeng/music_spider'
    scp_command = 'scp *.py  s3:%s' % s3_remote_path
    IsFailed = subprocess.call(scp_command, shell=True)
    if IsFailed:
        log_obj.write('%s sucess...\n' % scp_command)
    fab_command = 'fab -H s3 --keepalive=10 -- "cd %s; python main.py"' % s3_remote_path
    popen = subprocess.Popen(fab_command, shell=True, stdout=subprocess.PIPE)
    log_obj.write(popen.stdout.read())
mdev_fab()
