__author__ = 'huafeng'
#coding:utf-8
import os
import codecs
import re
PATH = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(PATH, 'all_vedio_name.txt')
ch_pattern = re.compile(ur"([\u4E00-\u9FA5]+)", re.U)
total_movie_set = set()
with codecs.open(filename, encoding='utf-8') as f:
    for line in f.readlines():
        for char in ch_pattern.findall(line):
            if len(char) <= 1:
                continue
            if len(char) >= 15:
                print char
            total_movie_set.add(char)
# codecs.open('filtered_vedio_name.txt', mode='wb', encoding='utf-8').writelines([item+'\n' for item in total_movie_set])
