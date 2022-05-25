import requests
from bs4 import BeautifulSoup

url = "https://www.maigoo.com/maigoo/2773hfs_index.html"

def get_Html():
    page_result = requests.get(url)
    html = BeautifulSoup(page_result.content, "html.parser")   
    return html
