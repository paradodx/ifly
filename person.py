from distutils.log import info
from email import message
import requests
import json
import os
from bs4 import BeautifulSoup
import lxml
from json import dumps


def ex_json(name):
    # 保存路径
    root = "D:\\ifly\\python\\humanHistory\\files\\"
    path = root + name + ".json"
    # 获取网页
    page_result = requests.get(url)
    html = BeautifulSoup(page_result.content, "html.parser")   
    # 保存页面元素数据
    res = {}
    # 寻找页面中class="descbox font16"的元素 分别有4个div 依次遍历
    for info_per in html.find_all(class_="descbox font16"):
        #第一个div中是人物的相关信息，遍历保存在小的list
        res.update({ele.find(class_='name').string: ele.find(class_='val').string for ele in info_per.find_all('li')})
        
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(res ,ensure_ascii=False))
    else:
        print("文件已存在!")


if __name__ == "__main__":
    url = "https://www.maigoo.com/mingren/2066.html"
    ex_json("杨振宁")