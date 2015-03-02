__author__ = 'huafeng'
#coding:utf-8
import requests
import os
import codecs
import time
from bs4 import BeautifulSoup
PATH = os.path.dirname(os.path.abspath(__file__))

def analysis_movie_name(url):
    # url = 'http://list.iqiyi.com/www/1/-------------4-1-1-iqiyi--.html'
    html = requests.get(url, timeout=20).text
    soup = BeautifulSoup(html)
    div_level_str = soup.find('div', class_='wrapper-piclist')
    li_level_list = div_level_str.find_all('li')
    # print len(li_level_list)
    title_list = [item.find('p', class_='site-piclist_info_title').text.strip() for item in li_level_list]
    # for title in title_list:
    #     print title.strip()
    return title_list

def get_all_movie():
    root_url = 'http://list.iqiyi.com'
    # url = 'http://list.iqiyi.com/www/1/-------------4-1-1-iqiyi--.html'#movie
    url = 'http://list.iqiyi.com/www/2/-------------4-1-1-iqiyi--.html'#tv
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    div_level_str = soup.find('div', class_='mod_sear_menu mt20 mb30')
    div_level_list = div_level_str.find_all('div')[1:]
    total_li_list = []
    [total_li_list.extend(item.find_all('li')) for item in div_level_list]
    url_str_list = [item.a['href'].strip() for item in total_li_list]
    url_pattern_list = [root_url + url.replace('4-1-1-iqiyi', '4-%s-1-iqiyi') for url in url_str_list if url.endswith('html')]
    print 'total_url count: ', len(url_pattern_list)
    for page_num in range(1, 31):
        print page_num,
        movie_title_list = []
        for url_pattern in url_pattern_list:
            try:
                url = url_pattern % page_num
            except:#抛异常，则说明单页
                url = url_pattern
            try:
                title_list = analysis_movie_name(url)
                movie_title_list.extend(title_list)
            except:
                pass
        tmp_set = set([item+'\n' for item in movie_title_list])
        print len(tmp_set)
        codecs.open('./aiqiyi/tv/aiqiyi_tv_%s.txt'%page_num, mode='wb', encoding='utf-8').writelines(tmp_set)
get_all_movie()
def combine_all_movie():
    import glob
    file_pattern = os.path.join(PATH, 'aiqiyi', 'tv','*')
    file_list = glob.glob(file_pattern)
    print 'total file count:', len(file_list)
    total_title_set = set()
    index = 0
    for filename in file_list:
        index += 1
        print index
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                total_title_set.add(line)
    print len(total_title_set)
    codecs.open(os.path.join(PATH, 'all_movie_name', 'aiqiyi_tv.txt'), mode='wb', encoding='utf-8').writelines(total_title_set)
# combine_all_movie()

