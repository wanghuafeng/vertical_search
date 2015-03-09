__author__ = 'huafeng'
#coding:utf-8
import subprocess

app_remote_path_on_s1 = '/home/gaius/wanghuafeng/app_spider'

scp_command = 'scp app_zip.py s1:%s' % app_remote_path_on_s1
subprocess.call(scp_command, shell=True)

fab_command = 'fab -H s1 --keepalive=10 -- "cd %s; python app_zip.py"' % app_remote_path_on_s1
subprocess.call(fab_command, shell=True)