from bs4 import BeautifulSoup

f = open('sample.txt', 'rt')
source = f.read()
soup = BeautifulSoup(source,'lxml')
titles = soup.find_all("td", class_="title")
for element in titles:
    print(element.a.get_text())
