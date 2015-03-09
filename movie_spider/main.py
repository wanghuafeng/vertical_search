__author__ = 'huafeng'
#coding:utf-8
import os
import re
import glob
import codecs
import time
import subprocess
from aiqiyi import get_aiqiyi_vedio
from souhu import get_sohu_vedio
from douban import get_douban_vedio
from vedio_360 import get_360_vedio

PATH = os.path.dirname(os.path.abspath(__file__))
unfiltered_sentence_filename = os.path.join(PATH, 'all_vedio_name.txt')
sentence_packet_filename = 'all_vedio_name.packet'
def combine_all_vedio():
    file_pattern = os.path.join('all_movie_name', '*')
    file_list = glob.glob(file_pattern)
    print 'file count in dir:', len(file_list)
    total_vedio_set = set()
    for filename in file_list:
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                total_vedio_set.add(line)
    print len(total_vedio_set)
    return total_vedio_set

def data_clean():
    ch_pattern = re.compile(ur"([\u4E00-\u9FA5]+)", re.U)
    total_movie_set = set()
    unfilter_total_vedio_set = combine_all_vedio()
    for vedio_name in unfilter_total_vedio_set:
        for char in ch_pattern.findall(vedio_name):
            if 1 < len(char) < 15:
                total_movie_set.add(char)
    codecs.open(unfiltered_sentence_filename, mode='wb', encoding='utf-8').writelines([item+'\n' for item in total_movie_set])
    print 'vedio combine and clean sucess...'

def sentence2Packet():
    remote_path = '/home/ferrero/cloudinn/filtered_unmatch_sentence'
    filter_path = '/home/ferrero/cloudinn/filtered_unmatch_sentence/prebuild_packet'
    mv_command = 'cp %s %s' % (unfiltered_sentence_filename, filter_path)
    IsFailed = subprocess.call(mv_command, shell=True)
    if IsFailed:
        print 'txt cp to %s failed...' % filter_path
    else:
        print 'txt cp to %s sucess...' % filter_path

    py_command = 'python {remote_path}/sentence2Packet.py -i {remote_path}/prebuild_packet/{sentence_filename}'.format(remote_path=remote_path, sentence_filename=os.path.basename(unfiltered_sentence_filename))#sentence文件的绝对路径
    IsFailed = subprocess.call(py_command, shell=True)
    if IsFailed:
        print '*.packet gen failed...'

def packet2horder(packet_base_filename):
    s3_packet_dirpath = '/home/ferrero/cloudinn/filtered_unmatch_sentence/prebuild_packet'
    packet_filename = os.path.join(s3_packet_dirpath, packet_base_filename)
    scp_command_s1 = 'scp %s s1:/home/gaius/horde_srv/tools/importer/auto/video' % packet_filename
    IsFailed = subprocess.call(scp_command_s1, shell=True)
    if IsFailed:
        print '*.packet scp from s3 to s1 failed...'
    else:
        print '*.packet spc from s3 to s1 sucess...'
    horde_command = 'bash /home/gaius/horde_srv/auto_import.sh video'
    fab_command = 'fab -H s1 --keepalive=10 -- "%s"' % horde_command
    subprocess.call(fab_command, shell=True)
if __name__ == "__main__":
    start_time = time.time()
    time_stamp = time.strftime("%Y_%m_%d_%H%M%S")
    print '****************start %s*******************' % time_stamp
    get_360_vedio()
    get_sohu_vedio()
    get_aiqiyi_vedio()
    get_douban_vedio()
    print 'vedio crawl ended, time consume:', time.time() - start_time
    data_clean()
    sentence2Packet()
    packet2horder(sentence_packet_filename)
    time_stamp = time.strftime("%Y_%m_%d_%H%M%S")
    print '****************end %s****************' % time_stamp

