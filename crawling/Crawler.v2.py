'''
A general crawler for Naver Webtoon

'''

import requests
import pickle
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup
from collections import namedtuple

# Method for creating a .txt file through requests and bs4

# I want to get all the td information from the naver webtoon list page. Do I need the html site? No.

Episode = namedtuple('Episode', ['no', 'img_url', 'title', 'rating', 'created_date'])


def open_webtoon_html(webtoon_id):
    naver_webtoon_base_link = 'http://comic.naver.com/webtoon/list.nhn'
    payload = {'titleId': webtoon_id}
    r = requests.get(naver_webtoon_base_link, params=payload)
    soup = BeautifulSoup(r.text, "lxml")
    return soup

def get_webtoon_information(webtoon_id):
    soup = open_webtoon_html(webtoon_id)
    tr_list = soup.find_all('tr')

    episode_list = list()
    for tr in tr_list:
        if tr.attrs == {'class': ['band_banner']} or tr.th:
            continue
        td_list = tr.find_all('td')

        # In order to find no, we go in to the a tag -> parse href -> from the query dictionary find 'no'
        td_list_a_tag = td_list[0].a
        parsed_a_tag = urlparse(td_list_a_tag['href'])
        no = parse_qs(parsed_a_tag.query)['no'][0]

        img_url = td_list[0].img['src'].strip()
        title = td_list[1].a.string.strip()
        rating = td_list[2].strong.string.strip()
        created_date = td_list[3].string.strip()
        episode = Episode(
            no=no,
            img_url=img_url,
            title=title,
            rating=rating,
            created_date=created_date
        )
        episode_list.append(episode)

    return episode_list

def save_episode_list_to_file(webtoon_id, episode_list):
    """
    episode_list로 전달된 Episode의 리스트를
    쉼표단위로 속성을 구분, 라인단위로 episode를 구분해 저장
    파일명은 <webtoon_id>_<가장 최근 에피소드no>_<가장 나중 에피소드no>.txt
    ex) 651673_1070_1050.txt

    ex)
    1070,http://...jpg,109화 - 무언가,9.93,2017.09.13
    1069,http://...jpg,109화 - 무언가,9.93,2017.09.13
    1068,http://...jpg,109화 - 무언가,9.93,2017.09.13
    1067,http://...jpg,109화 - 무언가,9.93,2017.09.13
    :param episode_list: Episode namedtuple의 list
    :param webtoon_id: 웹툰 고유 ID값 (str또는 int)
    :return:
    """
    filename = "{}_{}_{}".format(webtoon_id, episode_list[0].no, episode_list[-1].no)
    with open(filename, "wt") as f:
        for episode in episode_list:
            formatted_episode = '|'.join(episode)
            f.write(formatted_episode + "\n")

def load_episode_list_from_file(path):
    """
    path에 해당하는 file을 읽어 Episode리스트를 생성해 리턴
    1. file객체 f할당
    2. readline()함수를 이용해 한줄씩 읽기 <- 다른방법도 있습니다
    3. 한줄을 쉼표단위로 구분해서 Episode객체 생성
    4. 객체들을 하나의 리스트에 담아 리턴
    :param path:
    :return:
    """
    with open(path, "rt") as f:
        return [Episode._make(episode.strip().split('|')) for episode in f]


el= get_webtoon_information(119874)
print(el)
pickle.dump(el, open('yumi_pickle.txt', 'wb'))
# el = pickle.load(open('yumi_pickle.txt', 'rb'))