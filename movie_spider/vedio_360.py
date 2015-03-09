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

def get_vedio_list_by_pattern(url_pattern):
    '''由url_pattern获取其对应的vedio_list'''
    total_vedio_list = []
    for index in range(1, 21):
        # vedio_list= []
        print index
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
                # vedio_list.extend(title_list)
                total_vedio_list.extend(title_list)
            except:
                pass

    return total_vedio_list

def get_360_vedio():
    vedio_list = []
    pattern_list = [tv_pattern, movie_pattern]
    for pattern in pattern_list:
        pattern_vedio_list = get_vedio_list_by_pattern(pattern)
        vedio_list.extend(pattern_vedio_list)
    tmp_set = set([item+'\n' for item in vedio_list])
    codecs.open('all_movie_name/360.txt', mode='wb', encoding='utf-8').writelines(tmp_set)

if __name__ == "__main__":
    start_time = time.time()
    get_360_vedio()
    print time.time() - start_time
