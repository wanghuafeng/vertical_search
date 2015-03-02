__author__ = 'huafeng'
#coding:utf-8

import subprocess
s2_path = '/mnt/data/spiders/douban'

def exetract_title_from_html():

    scp_command = 'scp douban.py s2:%s' % s2_path

    subprocess.call(scp_command, shell=True)

    fab_command = 'fab -H s2 -- "cd %s; python douban.py"'%s2_path
    subprocess.call(fab_command, shell=True)

# scp_command = 'scp s2:%s/douban_movie_name.txt .' % s2_path
# subprocess.call(scp_command, shell=True)

def combine_all_vedio():
    import os
    import glob
    import codecs
    file_pattern = os.path.join('all_movie_name', '*')
    file_list = glob.glob(file_pattern)
    total_vedio_set = set()
    for filename in file_list:
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                total_vedio_set.add(line)
    print len(total_vedio_set)
    codecs.open('all_vedio_name.txt', mode='wb', encoding='utf-8').writelines(total_vedio_set)
combine_all_vedio()