import requests
from bs4 import BeautifulSoup
from collections import namedtuple


Episode = namedtuple('Episode', ['no', 'img_url', 'title', 'rating', 'created_date'])

def open_webtoon_html(webtoon_id):
    naver_webtoon_base_link = 'http://comic.naver.com/webtoon/list.nhn'
    payload = {'titleId': webtoon_id}
    r = requests.get(naver_webtoon_base_link, params=payload)
    soup = BeautifulSoup(r.text, "lxml")
    return soup
