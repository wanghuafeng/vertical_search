__author__ = 'huafeng'
#coding:utf-8
import os
import re
import time
import codecs
import subprocess
from book_jd import run
PATH = os.path.dirname(os.path.abspath(__file__))
unfiltered_sentence_filename = os.path.join(PATH, 'jd_book_name.txt')
sentence_packet_filename = 'jd_book_name.packet'

def data_clean(origin_filename=None):
    if not origin_filename:
        origin_filename = 'total_unsplite_book_name.text'
    char_pattern = re.compile( ur"([\u4E00-\u9FA5]+)", re.U)
    # char_book_name_filename = os.path.join('filetered_book_name.txt')
    exception_tuple = tuple( u'册 卷 下 装 节 张 辑 著 价 销 司 第 日 价 定 光盘 学习卡 票 版 载 修 拟 级 育 写 纲 赠 篇 邮 社 司 馆 品'.split())
    with codecs.open(origin_filename, encoding='utf-8') as f, \
    codecs.open(unfiltered_sentence_filename, mode='wb', encoding='utf-8') as wf:
        for line in f.readlines():
            for book_name in char_pattern.findall(line):
                if len(book_name) <= 1 or (book_name.endswith(exception_tuple)):
                    continue
                wf.write(book_name+'\n')

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
    start_time = time.time()
    time_stamp = time.strftime("%Y_%m_%d_%H%M%S")
    print '****************start %s*******************' % time_stamp
    run()
    print 'crawl ended, time consume:', time.time() - start_time
    data_clean()
    sentence2Packet()
    packet2horder(sentence_packet_filename, 'book')
    time_stamp = time.strftime("%Y_%m_%d_%H%M%S")
    print '****************end %s****************' % time_stamp

