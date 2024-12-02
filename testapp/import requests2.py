import requests
from bs4 import BeautifulSoup

r = requests.get("https://tengrinews.kz/")
s = BeautifulSoup(r.text, "html.parser")
items = s.find_all(class_="main-news_super_item")

for item in items:
    print(item.text.strip())