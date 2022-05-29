from distutils.log import info
from email import message
import requests
import json
import os
from bs4 import BeautifulSoup
import lxml
from json import dumps


def ex_json(name):
    root = "C:\\Users\\Ming\\Desktop\\讯飞\\maigoo\\files\\"
    path = root + name + ".json"
    page_result = requests.get(url)
    html = BeautifulSoup(page_result.content, "html.parser")   
    res = {}
    for info_per in html.find_all(class_="descbox font16"):
        res.update({ele.find(class_='name').string: ele.find(class_='val').string for ele in info_per.find_all('li')})
        
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(res ,ensure_ascii=False))
    else:
        print("文件已存在!")


if __name__ == "__main__":
    url = "https://www.maigoo.com/mingren/2066.html"
    ex_json("杨振宁")