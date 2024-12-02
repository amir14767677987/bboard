import requests
from sqlite3
from bs4 import BeautifulSoup as Soup

def parse_sit(url):
    r = requests.get(url)
    s = Soup(r.text, "html.pars")
    items = s.find_all(class_="main-news_super_item")
    return items

def main():
    url = "https://tengrinews.kz/"  
    items = parse_sit(url)  

    for item in items:
        link1 = item.find_all('a')  
        for link in link1:
            print(lin1.text) 
        
self.commit(url)


if _name_ == "_main_":
    main()