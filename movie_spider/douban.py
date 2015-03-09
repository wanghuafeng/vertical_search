__author__ = 'huafeng'
#coding:utf-8
import requests
import os
import glob
import codecs
import time
#
from bs4 import BeautifulSoup
PATH = os.path.dirname(os.path.abspath(__file__))
# url = 'http://movie.douban.com/subject/7916027/'
# html = requests.get(url).text
root_url = time.strftime('http://movie.douban.com/tag/%Y')

def anslysis_page_to_get_movie_names(url):
    try:
        html = requests.get(url, timeout=20).text
        soup = BeautifulSoup(html)
        div_content = soup.find('div', id='content')
        tr_level_list = div_content.find_all('tr', 'item')
        title_list = [item.find('a')['title'] for item in tr_level_list]
        return title_list
    except:
        return []

def get_douban_vedio():
    url_suffix = '?start=%s&type=T'
    html = requests.get(root_url, timeout=20).text
    soup = BeautifulSoup(html)
    page_div = soup.find('div', class_='paginator')
    total_page_count = page_div.find('span', class_='thispage')['data-total-page']
    total_movie_list = []
    for page_index in range(int(total_page_count) + 1):
        # print total_page_count, page_index
        url = root_url + url_suffix % (page_index*20)
        title_list = anslysis_page_to_get_movie_names(url)
        time.sleep(2)
        total_movie_list.extend(title_list)
    tmp_set = set([item + '\n' for item in total_movie_list])
    codecs.open('all_movie_name/douban.txt', mode='wb', encoding='utf-8').writelines(tmp_set)

if __name__ == "__main__":
    start_time = time.time()
    get_douban_vedio()
    print time.time() - start_time
