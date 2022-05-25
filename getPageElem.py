from getHtml import get_Html
import requests
from bs4 import BeautifulSoup 

def get_Elem(name):
    html = get_Html()
    news = html.find(class_='brand10 m1')
    desktop_path = "D:\\ifly\\python\\humanHistory\\files\\"
    full_path = desktop_path + name + ".txt"
    f = open(full_path,"wb+")
    f.write(news.text.encode("utf-8"))
    f.close

if __name__ ==  "__main__":
    get_Elem("save")