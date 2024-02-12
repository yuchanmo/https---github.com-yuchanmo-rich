import requests
import pandas as pd
from bs4 import BeautifulSoup


def getUpjongList():
    stock_base_url = 'https://finance.naver.com/'
    upjong_url = 'https://finance.naver.com/sise/sise_group.naver?type=upjong'
    response = requests.get(upjong_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    url_list = []
    for row in soup.select('tr a'):
        try:
            au_name = row.text
            au_link = row.get('href')
            if au_link.startswith('/sise'):
                url_list.append((au_name,stock_base_url+au_link))
        except Exception as e:
            print(e)
    return url_list
    
    
def getUpjongItemlist(upjong):    
    upjong_name,url = upjong
    res = requests.get(url)
    au_soup = BeautifulSoup(res.text, 'html.parser')
    item_url_list = []
    for row in au_soup.select('div.name_area a'):
        try:
            stock_name = row.text
            stock_link = row.get('href')
            if stock_link.startswith('/item/main'):
                item_url_list.append((upjong_name,stock_name,stock_link.split('=')[-1]))
        except Exception as e:
            print(e)
    return item_url_list

upjong_summary = []
upjong_list = getUpjongList()
for u in upjong_list:
    upjong_summary.extend(getUpjongItemlist(u))


df = pd.DataFrame(upjong_summary,columns=['category','name','code'])    
df.to_csv('upjong.csv')

