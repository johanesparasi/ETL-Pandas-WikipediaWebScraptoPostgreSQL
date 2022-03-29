import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

getHtml = requests.get('https://en.wikipedia.org/wiki/List_of_largest_banks').text
soup = BeautifulSoup(getHtml, 'lxml')
getData = soup.find_all('table', class_='wikitable sortable mw-collapsible')[2]

lst = []
marketcapRP = []

lst = [rec.text.strip() for rec in getData.find_all('td')]

rank = lst[0::3]
bank = lst[1::3]
getmarketcap = lst[2::3]

marketcapRP = [format(float(rec) * 14340.85 * 1000000000, '.3f') for rec in getmarketcap]

dict = {
    'Ranking': rank,
    'Bank' : bank,
    'Market Cap (in Rupiah)': marketcapRP
}

df = pd.DataFrame(dict)
df.set_index('Ranking', inplace=True)

try:
    engine = create_engine('postgresql://postgres:johanes@localhost:5432/pitonETL')
    df.to_sql('Wiki Web Scrapping', engine, if_exists='append')
    print('Success load into Database')
    print(df)
except Exception as e:
    print('Failed load into Database')
    print(e)