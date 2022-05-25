from cgitb import html
from getHtml import get_Html
import requests
from bs4 import BeautifulSoup
import os

def get_Pic():
    html = get_Html()
    img_src = html.find(class_="brand10 m1")
    Pic = 1
    for i in img_src.find_all("img"):
        root = "D:\\ifly\\python\\humanHistory\\imgs\\"
        path = root + "Picture" + str(Pic) + ".jpg"
        link = i.get("src")
        if not os.path.exists(path):
            if isinstance(link, str):
                    res = requests.get(link)
                    with open(path ,"wb") as fd:
                        fd.write(res.content)
                    Pic += 1
        else:
            print("文件已存在")

if __name__ ==  "__main__":
    get_Pic()
 