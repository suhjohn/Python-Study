import requests
from bs4 import BeautifulSoup

webtoon_url = 'http://comic.naver.com/webtoon/list.nhn?titleId=651673&weekday=sat'
source = requests.get(webtoon_url).text
print(source)

soup = BeautifulSoup(source)
print(soup.prettify())

f = open('sample.txt', 'wt')
f.write(soup.prettify())
f.close()
