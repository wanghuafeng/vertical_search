__author__ = 'huafeng'
#coding:utf-8
import requests
import os
import codecs
import time
from bs4 import BeautifulSoup

def analysis_url():
    hot_url_pattern = 'http://so.tv.sohu.com/list_p1100_p2_p3_p4_p5_p6_p77_p8_p9_p10%s_p11_p12_p131.html'
    new_url_pattern = 'http://so.tv.sohu.com/list_p1100_p2_p3_p4_p5_p6_p73_p8_p9_p10%s_p11_p12_p131.html'
    hot_tv_url_pattern = 'http://so.tv.sohu.com/list_p1101_p2_p3_p4_p5_p6_p7_p8_p9_p10%s_p11_p12_p13.html'
    new_tv_url_pattern = 'http://so.tv.sohu.com/list_p1101_p2_p3_p4_p5_p6_p73_p8_p9_p10%s_p11_p12_p13.html'
    movie_list = []
    for index in range(1, 53):
        print index
        url = new_tv_url_pattern % index
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html)
        div_level_str = soup.find('div', class_='sort-column area')
        ul_level_str = div_level_str.find('ul', class_='st-list cfix')
        li_level_list = ul_level_str.find_all('li')
        title_list = [item.strong.text for item in li_level_list]
        movie_list.extend(title_list)
        # print len(title_list)
        # for title in title_list:
        #     print title
    print len(movie_list)
    tmp_set = set([item+'\n' for item in movie_list])
    print len(tmp_set)
    codecs.open('souhu_tv_new.txt', mode='wb', encoding='utf-8').writelines(tmp_set)
# analysis_url()

def combine_tv():
    with codecs.open('souhu_tv_new.txt', encoding='utf-8') as f:
        new_tv_set = set(f.readlines())#1529
        print 'souhu_tv_new count: ', len(new_tv_set)
    with codecs.open('souhu_tv_hot.txt', encoding='utf-8') as f:
        hot_tv_set = set(f.readlines())#1529
        print 'souhu_tv_hot count: ', len(hot_tv_set)
    with codecs.open('sougou_tv.txt', mode='wb', encoding='utf-8') as wf:
        wf.writelines(hot_tv_set|new_tv_set)#1529
    print len(hot_tv_set|new_tv_set)
# combine_tv()
def combine_movie():
    with codecs.open('souhu_movie_new.txt', encoding='utf-8') as f:
        new_movie_set = set(f.readlines())#5936
    with codecs.open('souhu_movie_hot.txt', encoding='utf-8') as f:
        hot_movie_set = set(f.readlines())#5881
    with codecs.open('sougou_movie.txt', mode='wb', encoding='utf-8') as wf:
        wf.writelines(hot_movie_set|new_movie_set)#10074
    print len(hot_movie_set|new_movie_set)