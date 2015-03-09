__author__ = 'huafeng'
#coding:utf-8
import os
import codecs
import subprocess
s2_path = '/mnt/data/spiders/douban'

def exetract_title_from_html():

    scp_command = 'scp douban.py s2:%s' % s2_path

    subprocess.call(scp_command, shell=True)

    fab_command = 'fab -H s2 -- "cd %s; python douban.py"'%s2_path
    subprocess.call(fab_command, shell=True)

# scp_command = 'scp s2:%s/douban_movie_name.txt .' % s2_path
# subprocess.call(scp_command, shell=True)

def sentence2Packet_execute(sentence_filename, sentence_file_to_move = False, py_update = False):
    sentence_path, sentence_filename = os.path.split(sentence_filename)
    if not sentence_path:#若传值为相对路径，则设置sentence_path的默认路径
        sentence_path = '/home/ferrero/wanghuafeng/movie_spider'
    remote_path = '/home/ferrero/cloudinn/filtered_unmatch_sentence'
    IsScpFailed = True
    if py_update:#若过滤逻辑有改动，则此处将文件上传
        local_path = '/home/huafeng/PycharmProjects/filtered_unmatch_sentence/sentence2Packet.py'
        scp_command = 'scp {local_path} s3:{remote_path}'.format(local_path=local_path, remote_path=remote_path)
        print 'scp exectuing ...'
        IsScpFailed = subprocess.call(scp_command, shell=True)
    if sentence_file_to_move:#若有sentence文件需要生成.packet文件，则此处scp到s3
        # sentence_filename = "{sentence_path}/{sentence_filename}".format(sentence_path=sentence_path, sentence_filename=sentence_filename)
        scp_command = 'scp {sentence_path}/{sentence_filename} s3:{remote_path}/prebuild_packet/'.format(sentence_filename=sentence_filename, remote_path=remote_path, sentence_path=sentence_path)
        print scp_command
        print 'scp sentence file execting...'
        IsScpFailed = subprocess.call(scp_command, shell=True)

    if (not sentence_file_to_move) or (not IsScpFailed):#如果没有向服务器端移动文件，则不用判断IsScpFailed参数
        py_command = 'python {remote_path}/sentence2Packet.py -i {remote_path}/prebuild_packet/{sentence_filename}'.format(remote_path=remote_path, sentence_filename=sentence_filename)#sentence文件的绝对路径
        fab_command = 'fab -H s3 --keepalive=10 -- "{py_command}"'.format(py_command=py_command)
        subprocess.call(fab_command, shell=True)

def mdev_fab():
    log_obj = codecs.open('vedio.log', mode='ab')
    s3_remote_path = '/home/ferrero/wanghuafeng/movie_spider'
    scp_command = 'scp *.py  s3:%s' % s3_remote_path
    IsFailed = subprocess.call(scp_command, shell=True)
    if IsFailed:
        log_obj.write('%s sucess...\n' % scp_command)
    fab_command = 'fab -H s3 --keepalive=10 -- "cd %s; python main.py"' % s3_remote_path
    popen = subprocess.Popen(fab_command, shell=True, stdout=subprocess.PIPE)
    log_obj.write(popen.stdout.read())
mdev_fab()
