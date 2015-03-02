__author__ = 'huafeng'
#coding:utf-8
import os
import glob
import time
import codecs
import requests
from bs4 import BeautifulSoup

PATH = os.path.dirname(os.path.abspath(__file__))
area_list= range(10, 19)
cat_list = range(100, 119) + ['other']
year_list = range(2006, 2016) + ['other']

from itertools import product
decare_list = list(product(cat_list, year_list, area_list))


tv_pattern = 'http://www.360kan.com/dianshi/list.php?pageno={}&cat=%s&year=%s&area=%s'
movie_pattern = 'http://www.360kan.com/dianying/list.php?pageno={}&cat=%s&year=%s&area=%s'

def analysis_url(url_pattern):
    for index in range(1, 21):
        tv_list= []
        print index,
        url_parm = url_pattern.format(index)
        for param_tuple in decare_list:
            url = url_parm % param_tuple
            try:
                r = requests.get(url, timeout=20)
                html = r.text
                soup = BeautifulSoup(html)
                ul_level_str = soup.find('ul', class_='result-list clearfix')
                if not ul_level_str:
                    continue
                li_level_list = ul_level_str.find_all('li')
                title_list = [item.find('p', class_='video-title').a.text for item in li_level_list]
                tv_list.extend(title_list)
            except:
                pass
        total_tv_set = set([item+'\n' for item in  tv_list])
        print len(total_tv_set)
        codecs.open('./360_movie/360_movie_%s.txt'%index, mode='wb', encoding='utf-8').writelines(total_tv_set)
# analysis_url(movie_pattern)
def combine_all_tv_files():
    total_words_set = set()
    file_pattern = os.path.join(PATH, '360_movie', '360_movie*.txt')
    file_list = glob.glob(file_pattern)
    print 'len(file_list)', len(file_list)
    index = 0
    for filename in file_list:
        index += 1
        print index
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                total_words_set.add(line.strip())
    print 'len(total_words_set):', len(total_words_set)
    codecs.open('360_movie_combine.txt', mode='wb', encoding='utf-8').writelines([item+'\n' for item in total_words_set])
# combine_all_tv_files()