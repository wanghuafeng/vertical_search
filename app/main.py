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
# sentence_packet_filename = 'music.packet'

def data_clean(filename=None):
    if not filename:
        filename = 'app_download.txt'
    filter_pattern = re.compile(ur"([^\u4E00-\u9FA5\da-zA-Z\s]+)", re.U)
    blank_pattern = re.compile(ur"(\s+)", re.U)
    num_letter_filter_pattern = re.compile(ur"([^a-zA-Z\d\s]+)", re.U)
    total_movie_set = set()
    unfilter_total_vedio_set  = set(codecs.open(filename, encoding='utf-8').readlines())
    for line in [item.strip().lower() for item in unfilter_total_vedio_set]:
        if not line:
            continue
        if not filter_pattern.search(line):#数字+字母+汉字+空格
            if not num_letter_filter_pattern.search(line):#数字+字母+空格
                total_movie_set.add(line)
            else:
                filtered_line = blank_pattern.sub('', line)#汉字+字母/数字/空格
                total_movie_set.add(filtered_line)
    codecs.open(unfiltered_sentence_filename, mode='wb', encoding='utf-8').writelines([item+'\n' for item in total_movie_set])
    print 'music combine and clean sucess...'

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
    fab_command = 'fab -H s1 --keepalive=10 -- "%s"' % horde_command
    subprocess.call(fab_command, shell=True)

if __name__ == "__main__":
    # start_time = time.time()
    # time_stamp = time.strftime("%Y_%m_%d_%H%M%S")
    # print '****************start %s*******************' % time_stamp
    # run()
    # print 'crawl ended, time consume:', time.time() - start_time
    # data_clean()
    # sentence2Packet()
    packet2horder(sentence_packet_filename, 'music')
    # time_stamp = time.strftime("%Y_%m_%d_%H%M%S")
    # print '****************end %s****************' % time_stamp
    #
