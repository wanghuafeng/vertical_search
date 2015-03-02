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

def analyse_html(html):
    soup = BeautifulSoup(html)
    div_level_str = soup.find('div', id='content')
    title = div_level_str.h1.span.text
    return title.strip()

def get_all_titles():
    file_pattern = os.path.join(PATH, 'html', '*.html')
    file_list = glob.glob(file_pattern)
    total_title_set = set()
    title_count = len(file_list)
    index = 0
    for filename in file_list:
        index += 1
        print index, title_count
        with open(filename) as f:
            html = f.read()
            try:
                title = analyse_html(html)
                total_title_set.add(title)
            except:
                print filename

    codecs.open('douban_movie_name.txt', mode='wb', encoding='utf-8').writelines([item + '\n' for item in total_title_set])
get_all_titles()