import requests
import pandas as pd
from bs4 import BeautifulSoup


def getThemeList():
    stock_base_url = 'https://finance.naver.com'
    url_set = set()
    loop_flag = True
    idx = 1
    for i in range(1,30):
        url = f'https://finance.naver.com/sise/theme.naver?&page={i}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')    
        for row in soup.select('tr a'):
            try:
                au_name = row.text
                au_link = row.get('href')
                pair = (au_name,stock_base_url+au_link)
                if pair in url_set:
                    loop_flag=False
                    break
                if au_link.startswith('/sise') and au_link.find('page=')<0:
                    url_set.add((idx, au_name,stock_base_url+au_link))
                    idx+=1
            except Exception as e:
                print(e)
        if not loop_flag:
            break
    return sorted(url_set,key=lambda x : x[0])

    
def getThemeItemlist(theme):    
    _,sector_name,url = theme
    res = requests.get(url)
    au_soup = BeautifulSoup(res.text, 'html.parser')
    item_url_list = []
    for row in au_soup.select('div.name_area a'):
        try:
            stock_name = row.text
            stock_link = row.get('href')
            if stock_link.startswith('/item/main'):
                item_url_list.append((sector_name,stock_name,stock_link.split('=')[-1]))
        except Exception as e:
            print(e)
    return item_url_list

theme_summary = []
theme_list = getThemeList()
for u in theme_list:
    theme_summary.extend(getThemeItemlist(u))

df = pd.DataFrame(theme_summary,columns=['category','name','code'])    
df.to_csv('theme.csv')

