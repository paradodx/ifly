from cgitb import html
from numpy import save
import requests,json,os,lxml
from bs4 import BeautifulSoup
from json import dumps

# 获取页面 
def getHtml(url):
    page_result = requests.get(url)
    html = BeautifulSoup(page_result.content, "html.parser") 
    return html

# 保存页面
def saveHtml(name):
    root = "C:\\Users\\Ming\\Desktop\\讯飞\\maigoo\\files\\"
    path = root + name + ".html"
    f = open(path,"wb+")
    f.write(str(html))
    f.close

# 保存人物页面 (读取本地？)
def saveHtml_human():
    root = "C:\\Users\\Ming\\Desktop\\讯飞\\maigoo\\files\\list\\"
    page = 1
    for i in html.find_all("a", class_="title font20 c333 b dhidden"):
        link = i.get("href")
        path = root + "人物" + str(page) + ".html"
        if isinstance(link,str):
            res = requests.get(link)
            with open(path, 'wb') as f:
                    f.write(res.content)
                    page += 1
        else:
            print("文件已存在!")

# 解析页面
def parseHtml(name):
    print()


if __name__ == "__main__":
    baseUrl = "https://www.maigoo.com/mingren/list_2773.html"
    html = getHtml(baseUrl)
    saveHtml("合肥名人")
    saveHtml_human()