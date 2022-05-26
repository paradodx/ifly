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
    listBig = []
    listSmall = []
    # 寻找页面中class="descbox font16"的元素 分别有3个div 依次遍历
    for info_per in html.find_all(class_="descbox font16"):
        #第一个div中是人物的相关信息，遍历保存在小的list
        for link in info_per.find_all(class_="val"):
            i = link.get_text() # 提取文本
            listSmall.append(i)
        # 3个div元素保存在大list
        text = info_per.get_text() 
        listBig.append(text)


    req_name = listSmall[0]
    req_gender = listSmall[1]
    req_nation = listSmall[2]
    req_nations = listSmall[3]
    req_birthPlace = listSmall[4]
    req_birthDay = listSmall[5]
    req_ani = listSmall[6]
    req_college = listSmall[7]
    req_person = listBig[1]
    req_social = listBig[2]
    req_title = listBig[3]

    data_dict = {
        "中文名": req_name,
        "性别": req_gender,
        "国籍": req_nation,
        "民族": req_nations,
        "出生地": req_birthPlace,
        "出生日期": req_birthDay,
        "生肖": req_ani,
        "毕业院校": req_college,
        "任务履历": req_person,
        "社会任职": req_social,
        "荣誉称号": req_title
    }

    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data_dict,ensure_ascii=False))
    else:
        print("文件已存在!")


if __name__ == "__main__":
    url = "https://www.maigoo.com/mingren/2066.html"
    ex_json("杨振宁")