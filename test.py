import requests
from bs4 import BeautifulSoup
from file_utils import *
from request_util import *

url = 'http://ren.bytravel.cn/Celebrity/index392_list9.html'
res =requests.get(url)

coding = 'gbk'
try:
    text = str(res.text.encode('ISO-8859-1'), encoding='gbk')
except:
    coding = 'utf-8'
    text = BeautifulSoup(res.content, 'html.parser', from_encoding='gb18030').prettify()

soup=BeautifulSoup(text, 'html.parser')
save_data(file_name='test.txt', info=soup.prettify(), coding='utf-8')
# soup.find(id='page_left').find(style='float:right ').select('td')
# title=soup.select('#artibody')[0].text
soup = BeautifulSoup(open('test.txt', encoding='utf-8'), 'lxml')
a = soup.find(id='page_left')

for ele in a.find(style='float:right ').select('td'):
    if ele.find('strong'):
        print(ele.text)

for ele in a.find(''):
    print(ele)