from bs4 import BeautifulSoup


f = open('full_webtoon_html.txt', 'rt')

source = f.read()

webtoon_table = soup.select_one('table.viewList')

