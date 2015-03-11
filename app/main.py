__author__ = 'huafeng'
#coding:utf-8
import os
import re
import glob
import codecs
import time
import subprocess
from app_360 import run
PATH = os.path.dirname(os.path.abspath(__file__))
unfiltered_sentence_filename = os.path.join(PATH, 'app_download_cleaned.txt')
sentence_packet_filename = 'app_download_cleaned.packet'
prebuild_filename = 'app_download_cleaned.prebuild'
build_filename = 'vs_app_360.build'
def data_clean(filename=None):
    if not filename:
        filename = 'app_download.txt'
    bracket_filter_pattern = re.compile(ur'[\(\（].*[\)\）]')
    char_pattern = re.compile( ur"([^\u4E00-\u9FA5]+)", re.U)
    num_letter_pattern = re.compile( ur"([\da-zA-Z]+)", re.U)
    blank_pattern = re.compile(ur"\s+", re.U)
    total_app_name_set = set()
    unfilter_total_vedio_set  = set(codecs.open(filename, encoding='utf-8').readlines())
    for line in [item.strip().lower() for item in unfilter_total_vedio_set]:
        if not line:
            continue
        if bracket_filter_pattern.search(line):#若含有括号
            line = bracket_filter_pattern.sub('', line)
        splited_line = line.split('\t')
        app_name = splited_line[0]
        freq = splited_line[-1]
        if not num_letter_pattern.search(app_name):#无数字/字母
            if blank_pattern.search(line):
                for app in blank_pattern.split(app_name):
                    app_line = app + '\t' + freq
                    total_app_name_set.add(app_line)
        else:
            total_app_name_set.add(line)
    codecs.open(unfiltered_sentence_filename, mode='wb', encoding='utf-8').writelines([item+'\n' for item in total_app_name_set])
    print 'txt combine and clean sucess...'

def sentence2Packet():
    remote_path = '/home/ferrero/cloudinn/filtered_unmatch_sentence'
    filter_path = '/home/ferrero/cloudinn/filtered_unmatch_sentence/prebuild_packet'
    mv_command = 'cp %s %s' % (unfiltered_sentence_filename, filter_path)
    IsFailed = subprocess.call(mv_command, shell=True)
    if IsFailed:
        print 'txt cp to %s failed...' % filter_path
    else:
        print 'txt cp to %s sucess...' % filter_path

    py_command = 'python {remote_path}/sentence2Packet_with_num_letter.py -i {remote_path}/prebuild_packet/{sentence_filename}'.format(remote_path=remote_path, sentence_filename=os.path.basename(unfiltered_sentence_filename))#sentence文件的绝对路径
    IsFailed = subprocess.call(py_command, shell=True)
    if IsFailed:
        print '*.packet gen failed...'

def prebuild2build():
    filter_path = '/home/ferrero/cloudinn/filtered_unmatch_sentence/prebuild_packet'
    abs_prebuild_filename = os.path.join(filter_path, prebuild_filename)
    abs_build_filename = os.path.join(filter_path, build_filename)
    with codecs.open(abs_prebuild_filename, encoding='utf-8') as f:
        codecs.open(abs_build_filename, mode='wb', encoding='utf-8').writelines(f.readlines())
    udb1_build_to_cloud_path = '/data/cloud/daily_data'#云词
    udb1_vertical_path = '/data/vertical/builds/current'#垂直搜索
    scp_command = 'scp %(abs_build_filename)s udb1:%(cloud_path)s; scp %(abs_build_filename)s udb1:%(vertical_path)s' % {"abs_build_filename":abs_build_filename, "cloud_path":udb1_build_to_cloud_path, 'vertical_path':udb1_vertical_path}
    IsFailed = subprocess.call(scp_command, shell=True)
    if not IsFailed:
        print '.build scp from s3 to udb1 sucess...'
    else:
        print '.build scp form s3 to udb1 failed...'

def packet2horder(packet_base_filename, catagory):
    s3_packet_dirpath = '/home/ferrero/cloudinn/filtered_unmatch_sentence/prebuild_packet'
    packet_filename = os.path.join(s3_packet_dirpath, packet_base_filename)
    scp_command_s1 = 'scp %s s1:/home/gaius/horde_srv/tools/importer/auto/%s' % (packet_filename, catagory)
    IsFailed = subprocess.call(scp_command_s1, shell=True)
    if IsFailed:
        print '*.packet scp from s3 to s1 failed...'
    else:
        print '*.packet spc from s3 to s1 sucess...'
    horde_command = 'bash /home/gaius/horde_srv/auto_import.sh %s' % catagory
    fab_command = '/usr/local/bin/fab -H s1 --keepalive=10 -- "%s"' % horde_command
    subprocess.call(fab_command, shell=True)

if __name__ == "__main__":
    data_clean()
    start_time = time.time()
    time_stamp = time.strftime("%Y_%m_%d_%H%M%S")
    print '****************start %s*******************' % time_stamp
    run()
    print 'crawl ended, time consume:', time.time() - start_time
    data_clean()
    sentence2Packet()
    prebuild2build()
    time_stamp = time.strftime("%Y_%m_%d_%H%M%S")
    print '****************end %s****************' % time_stamp
