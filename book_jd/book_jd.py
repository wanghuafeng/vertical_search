__author__ = 'huafeng'
#coding:utf-8
import os
import re
import time
import codecs
import urllib2
import requests
from bs4 import BeautifulSoup

PATH = os.path.dirname(os.path.abspath(__file__))
def parse_topic_url():
    book_url = "http://book.jd.com/booksort.html"
    response = urllib2.urlopen(book_url)
    html = response.read()
    soup = BeautifulSoup(html)
    div_level_str = soup.find('div', id='booksort')
    em_level_list = div_level_str.find_all('em')
    topic_url_list = [item.a['href'] for item in em_level_list]
    print topic_url_list[32:-2],len(set(topic_url_list))
    return topic_url_list[32:-2]
# parse_topic_url()
def gen_whole_page_url(book_page_url_filename):
    topic_url_list = parse_topic_url()
    # book_page_url_filename = os.path.join(PATH, 'jd_whole_page_url')
    with codecs.open(book_page_url_filename, mode='wb', encoding='utf-8') as wf_page_url:
        count = 0
        for topic_url in topic_url_list:
            count += 1
            page_url_list = []
            response = requests.get(topic_url, timeout=10)
            html = response.text
            soup = BeautifulSoup(html)
            max_page_str = soup.find('div', class_='pagin pagin-m')
            if not max_page_str:
                print 'max_page_str do not match regular expression in url:%s'%topic_url
                continue
            page_size = max_page_str.span.text.split('/')[-1]
            print count, page_size
            end_url_pattern = '?s=15&t=1&p=%s'
            for page_num in range(1, int(page_size)+1):
                url = ''.join((topic_url,end_url_pattern%page_num))
                page_url_list.append(url+'\n')
            wf_page_url.writelines(page_url_list)
# start_time = time.time()
# gen_whole_page_url()
# print time.time() - start_time
def analysis_page_url_to_get_pagesize():
        page_url = 'http://list.jd.com/1713-3265-3429.html'
        html = requests.get(page_url, timeout=10).text
        soup = BeautifulSoup(html)
        max_page_str = soup.find('div', class_='pagin pagin-m')
        print max_page_str
        if not max_page_str:
            print 'max_page_str is null'
            return
        page_size = max_page_str.span.text.split('/')[-1]
        print page_size
        end_url_pattern = '?s=15&t=1&p=%s'
        for page_num in range(1, int(page_size)+1):
            url = ''.join((page_url,end_url_pattern%page_num))
            print url
# read_topic_page_url_to_get_pagesize()

def get_bookname_by_page_url(url):
    '''解析Page_url获取该页面所有图书名'''
    page_book_list = []
    try:
        r = requests.get(url, timeout=15)
        html = r.text
        soup = BeautifulSoup(html)
        book_name_str_list = soup.find_all('dt', class_='p-name')
        book_name_list = [item.a['title'].strip() for item in book_name_str_list]
        page_book_list.extend([item.encode('ISO-8859-1').decode('gbk') for item in book_name_list])
    except:
        pass
    return page_book_list
# url = 'http://list.jd.com/1713-3291-6621.html'
# get_bookname_by_page_url(url)
def run():
    book_page_url_filename = os.path.join(PATH, 'jd_whole_page_url')
    gen_whole_page_url(book_page_url_filename)
    book_name_filename = os.path.join(PATH, 'total_unsplite_book_name.txt')
    with codecs.open(book_page_url_filename, encoding='utf-8') as f, \
    codecs.open(book_name_filename, mode='wb', encoding='utf-8') as wf:
        for url_str in f.readlines():
            url = url_str.rstrip()
            page_book_list = get_bookname_by_page_url(url)
            wf.writelines([item+'\n' for item in page_book_list])




