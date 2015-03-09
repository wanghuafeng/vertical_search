__author__ = 'huafeng'
#coding:utf-8
import os
import re
import time
import codecs
import requests
from bs4 import BeautifulSoup

root_url = 'http://zhushou.360.cn'
soft_url = 'http://zhushou.360.cn/list/index/cid/1'
game_url = 'http://zhushou.360.cn/list/index/cid/2'
num_pattern = re.compile('\d+')
url_suffix = '?page=%s'
def get_catagory_urls():
    total_catagory_url_list = []
    for url in [soft_url, game_url]:
        try:
            html = requests.get(url, timeout=20).text
            soup = BeautifulSoup(html)
            ul_level_str = soup.find('ul', class_='select')
            catogary_url_list = [root_url+url_str['href'] for url_str in ul_level_str.li.find_all('a')]
            total_catagory_url_list.extend(catogary_url_list)
        except:
            print 'root url: %s crawl failed...' % url
    print 'total_catagory_url_list len:', len(total_catagory_url_list)
    return total_catagory_url_list
# get_catagory_urls()

def get_page_size_by_catagory_url(url):
    try:
        html = requests.get(url, timeout=20).text
        soup = BeautifulSoup(html)
        page_str = soup.find('script', text=re.compile('page'))
        page_count_str = page_str.text.strip()
        return re.search('pg.pageCount = (\d+)', page_count_str).group(1)
    except:
        print 'page_num get failed on url: %s' % url
        return None
# url = 'http://zhushou.360.cn/list/index/cid/11/'
# print get_page_size_by_catagory_url(url)

def get_all_page_urls():
    catagory_url_list = get_catagory_urls()
    total_page_url_list = []
    for catagory_url in catagory_url_list:
        page_size = get_page_size_by_catagory_url(catagory_url)
        if page_size:
            page_url_list = [catagory_url+url_suffix%page_index for page_index in range(int(page_size)+1)]
            total_page_url_list.extend(page_url_list)
    return total_page_url_list
# get_all_page_urls()

def analysis_page(url):
    app_download_str_list = []
    try:
        html = requests.get(url, timeout=20).text
        soup = BeautifulSoup(html)
        ul_level_list = soup.find('ul', id='iconList')
        li_list = [item for item in ul_level_list.find_all('li')]
    except:
        print 'page_url %s crawl failed...' % url
        return app_download_str_list
    for li_str in li_list:
        try:
            app_name = li_str.h3.text
            download_str = li_str.span.text.replace(u'万', '0000').replace(u'千', '000').replace(u'亿', '00000000')
            download_count = num_pattern.search(download_str).group()
            app_download_str_list.append(app_name+'\t' + download_count)
        except:
            pass
    return app_download_str_list

def run():
    total_page_url_list = get_all_page_urls()
    total_page_url_count = len(total_page_url_list)#1126
    print 'total_page_url count', len(total_page_url_list)
    app_download_list = []
    index = 0
    for page_url in total_page_url_list:
        index += 1
        page_app_list = analysis_page(page_url)
        print index, total_page_url_count, len(page_app_list)
        app_download_list.extend(page_app_list)
    codecs.open('app_download_origin.txt', mode='wb', encoding='utf-8').writelines(set([item+'\n' for item in app_download_list]))
# start_time = time.time()
# run()
# print time.time() - start_time
