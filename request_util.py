import requests
from file_utils import save_data
from string_utils import neat_url
import os
from bs4 import BeautifulSoup


def get_headers():
    headers = {
        'Content-Type': 'application/json'
        }
    return headers


def get(url=''):
    return requests.get(url=url, headers=get_headers())


def get_html_path(url='', html_dir='data/html', web=''):
    if web:
        html_dir = f'{html_dir}/{web}'
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)

    file_name = f'{html_dir}/{neat_url(url)}.html'
    if os.path.exists(file_name):
        return file_name

    res = get(url)
    # coding = 'gbk'
    # try:
    #     text = str(res.text.encode('ISO-8859-1'), encoding='gbk')
    # except:
    #     coding = 'utf-8'
    text = BeautifulSoup(res.content, 'html.parser', from_encoding='gb18030').prettify()
    save_data(file_name=file_name, info=text, coding='utf-8')
    return file_name


def post(url=''):
    data = {}
    return requests.post(url, json=data, headers=get_headers()).json()


