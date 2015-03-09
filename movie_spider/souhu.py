__author__ = 'huafeng'
#coding:utf-8
import requests
import os
import codecs
import time
from bs4 import BeautifulSoup

movie_hot_url_pattern = 'http://so.tv.sohu.com/list_p1100_p2_p3_p4_p5_p6_p77_p8_p9_p10%s_p11_p12_p131.html'
movie_new_url_pattern = 'http://so.tv.sohu.com/list_p1100_p2_p3_p4_p5_p6_p73_p8_p9_p10%s_p11_p12_p131.html'
hot_tv_url_pattern = 'http://so.tv.sohu.com/list_p1101_p2_p3_p4_p5_p6_p7_p8_p9_p10%s_p11_p12_p13.html'
new_tv_url_pattern = 'http://so.tv.sohu.com/list_p1101_p2_p3_p4_p5_p6_p73_p8_p9_p10%s_p11_p12_p13.html'

def analysis_url(url_pattern, range_end):
    vedio_list = []
    for index in range(1, range_end):
        # print index
        url = url_pattern % index
        try:
            r = requests.get(url, timeout=20)
            html = r.text
            soup = BeautifulSoup(html)
            div_level_str = soup.find('div', class_='sort-column area')
            ul_level_str = div_level_str.find('ul', class_='st-list cfix')
            li_level_list = ul_level_str.find_all('li')
            title_list = [item.strong.text for item in li_level_list]
            vedio_list.extend(title_list)
        except:
            pass
    return vedio_list

def get_sohu_vedio():
    total_vedio_list = []
    #电影（对外开放:page=200）,电视剧(对外开放:page=53)
    url_pattern_list = [(hot_tv_url_pattern, 53), (movie_hot_url_pattern, 201), (movie_new_url_pattern, 201), (new_tv_url_pattern, 53)]
    for url_pattern_tuple in url_pattern_list:
        vedio_list = analysis_url(url_pattern_tuple[0], range_end=url_pattern_tuple[1])
        total_vedio_list.extend(vedio_list)
    tmp_set = set([item+'\n' for item in total_vedio_list])
    codecs.open('all_movie_name/souhu.txt', mode='wb', encoding='utf-8').writelines(tmp_set)

if __name__ == "__main__":
    start_time = time.time()
    get_sohu_vedio()
    print time.time() - start_time