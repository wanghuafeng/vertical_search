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

movie_url = 'http://list.iqiyi.com/www/1/-------------4-1-1-iqiyi--.html'#movie
tv_url = 'http://list.iqiyi.com/www/2/-------------4-1-1-iqiyi--.html'#tv

def get_vedio_by_url(url):
    root_url = 'http://list.iqiyi.com'
    vedio_list = []
    html = requests.get(url, timeout=20).text
    soup = BeautifulSoup(html)
    div_level_str = soup.find('div', class_='mod_sear_menu mt20 mb30')
    div_level_list = div_level_str.find_all('div')[1:]
    total_li_list = []
    [total_li_list.extend(item.find_all('li')) for item in div_level_list]
    url_str_list = [item.a['href'].strip() for item in total_li_list]
    url_pattern_list = [root_url + url.replace('4-1-1-iqiyi', '4-%s-1-iqiyi') for url in url_str_list if url.endswith('html')]
    # print 'total_url count: ', len(url_pattern_list)
    for page_num in range(1, 31):
        # print page_num
        for url_pattern in url_pattern_list:
            try:
                url = url_pattern % page_num
            except:#抛异常，则说明单页
                url = url_pattern
            try:
                title_list = analysis_movie_name(url)
                vedio_list.extend(title_list)
            except:
                pass
    return vedio_list

def get_aiqiyi_vedio():
    total_vedio_list = []
    vedio_url_list = [movie_url, tv_url]
    for url in vedio_url_list:
        try:
            vedio_list = get_vedio_by_url(url)
        except:
            continue
        total_vedio_list.extend(vedio_list)
    tmp_set = set([item+'\n' for item in total_vedio_list])
    codecs.open('all_movie_name/aiqiyi.txt', mode='wb', encoding='utf-8').writelines(tmp_set)

if __name__ == "__main__":
    start_time = time.time()
    get_aiqiyi_vedio()
    print time.time() - start_time