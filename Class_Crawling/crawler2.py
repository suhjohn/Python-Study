"""
class NaverWebtoonCrawler생성
    초기화메서드
        webtoon_id
        episode_list (빈 list)
            를 할당
    인스턴스 메서드
        def get_episode_list(self, page)
            해당 페이지의 episode_list를 생성, self.episode_list에 할당
        def clear_episode_list(self)
            자신의 episode_list를 빈 리스트로 만듬
        def get_all_episode_list(self)
            webtoon_id의 모든 episode를 생성
        def add_new_episode_list(self)
            새로 업데이트된 episode목록만 생성
"""
import os
import pickle
from urllib.parse import urlparse, parse_qs
from webtoon import Webtoon

import requests
import utils
from bs4 import BeautifulSoup


class NaverWebtoonCrawler:
    def __init__(self, webtoon_title=None):
        # find_webtoon()메서드에 초기화 메서드에 주어진 webtoon_title매개변수를 사용
        # 검색결과를 webtoon_search_results변수에 할당 (리스트)
        webtoon_search_results = self.find_webtoon(webtoon_title)

        # 검색결과가 없을 경우
        while not webtoon_search_results:
            search_title = input('검색할 웹툰명을 입력해주세요: ')
            webtoon_search_results = self.find_webtoon(search_title)

        # 검색결과가 1개일 경우, self.webtoon을 바로 지정
        if len(webtoon_search_results) == 1:
            self.webtoon = webtoon_search_results[0]

        # 2개 이상일 경우, 선택하도록 함
        elif len(webtoon_search_results) >= 2:
            while True:
                print('웹툰을 선택해주세요')
                for index, webtoon in enumerate(webtoon_search_results):
                    print(' {}. {}'.format(index + 1, webtoon.title))
                try:
                    selected_index = int(input('- 선택: '))
                    self.webtoon = webtoon_search_results[selected_index - 1]
                    break
                except IndexError:
                    print('에러] {}번 이하의 숫자를 선택해주세요\n'.format(
                        len(webtoon_search_results)
                    ))
                except ValueError:
                    print('에러] 해당 웹툰의 숫자를 입력해주세요\n')
        """
        1. webtoon_title이 주어지면,
            1-1. 해당 웹툰 검색결과를 가져와서
            1-2. 검색결과가 1개면 해당 웹툰을
                  self.webtoon에 할당
            1-3. 검색결과가 2개 이상이면 선택가능하도록 목록을 보여주고
                  input으로 입력받음
            1-4. 검색결과가 없으면 다시 웹툰을 검색하도록 함
        2. webtoon_title이 주어지지 않으면
            2-1. 웹툰 검색을 할 수 있는 input을 띄워줌
            2-2. 이후는 위의 1-2, 1-3을 따라감
        3. webtoon_id를 쓰던 코드를 전부 수정 (self.webtoon을 사용)
            self.webtoon은 Webtoon타입 namedtuple
        """

        self.webtoon.get_description()
        # 객체 생성 시, 'db/{webtoon_id}.txt'파일이 존재하면
        # 바로 load() 해오도록 작성
        self.episode_list = list()
        self.load(init=True)
        print('- 현재 웹툰: %s' % self.webtoon.title)
        print('- 로드된 Episode수: %s' % len(self.episode_list))
        self.webtoon_id_title_dict = dict()

    @property
    def total_episode_count(self):
        """
        webtoon_id에 해당하는 실제 웹툰의 총 episode수를 리턴
        requests를 사용
        :return: 총 episode수 (int)
        """
        el = utils.get_webtoon_episode_list(self.webtoon)
        return int(el[0].no)

    @property
    def up_to_date(self):
        """
        현재 가지고있는 episode_list가 웹상의 최신 episode까지 가지고 있는지
        1. cur_episode_count = self.episode_list의 개수
        2. total_episode_count = 웹상의 총 episode 개수
        3. 위 두 변수의 값이 같으면 return True, 아니면 return False처리
        :return: boolean값
        """
        # 지금 가지고 있는 총 Episode의 개수
        #   self.episode_list에 저장되어있음
        #      -> list형 객체
        #      -> list형 객체의 길이를 구하는 함수(시퀀스형 객체는 모두 가능)
        #        -> 내장함수 len(s)
        # cur_episode_count = len(self.episode_list)

        # 웹상의 총 episode개수
        # total_episode_count = self.total_episode_count

        # 두 값이 같으면 True를, 아니면 False를 리턴
        # if cur_episode_count == total_episode_count:
        #     return True
        # return False
        # return cur_episode_count == total_episode_count
        return len(self.episode_list) == self.total_episode_count

    def find_webtoon(self, title):
        """
        title에 주어진 문자열로 get_webtoon_list로 받아온 웹툰 목록에서
        일치하거나 문자열이 포함되는 Webtoon목록을 리턴
        :param title: 찾을 웹툰 제목
        :return: list(Webtoon)
        """
        # results = []
        # webtoon_list = self.get_webtoon_list()
        # for webtoon in webtoon_list:
        #     if title in webtoon.title:
        #         results.append(webtoon)
        # return results
        return [webtoon for webtoon in
                self.get_webtoon_list()
                if title in webtoon.title]

    def get_webtoon_list(self):
        """
        네이버웹툰의 모든 웹툰들을 가져온다
        :return:
        """
        url = 'http://comic.naver.com/webtoon/weekday.nhn'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        webtoon_list = set()

        daily_all = soup.select_one('.list_area.daily_all')
        days = daily_all.select('div.col')

        for day in days:
            items = day.select('li')
            for item in items:
                img_url = item.select_one('div.thumb').a.img['src']
                title = item.select_one('a.title').get_text(strip=True)
                url_webtoon = item.select_one('a.title')['href']

                parse_result = urlparse(url_webtoon)
                queryset = parse_qs(parse_result.query)
                title_id = queryset['titleId'][0]

                webtoon = Webtoon(title_id, img_url, title)
                webtoon_list.add(webtoon)


        webtoon_list = sorted(list(webtoon_list), key=lambda webtoon: webtoon.title)
        return webtoon_list

    def update_episode_list(self, force_update=False):
        """
        1. recent_episode_no = self.episode_list에서 가장 최신화의 no
        2. while문 또는 for문 내부에서 page값을 늘려가며
            utils.get_webtoon_episode_list를 호출
            반환된 list(episode)들을 해당 episode의 no가
                recent_episode_no보다 클 때 까지만 self.episode_list에 추가
        self.episode_list에 존재하지 않는 episode들을 self.episode_list에 추가
        :param force_update: 이미 존재하는 episode도 강제로 업데이트
        :return: 추가된 episode의 수 (int)
        """
        if force_update:
            self.episode_list = list()
        recent_episode_no = self.episode_list[0].no if self.episode_list else 0
        print('- Update episode list start (Recent episode no: %s) -' % recent_episode_no)
        page = 1
        new_list = list()
        while True:
            print('  Get webtoon episode list (Loop %s)' % page)
            # 계속해서 증가하는 'page'를 이용해 다음 episode리스트들을 가져옴
            el = utils.get_webtoon_episode_list(self.webtoon, page)
            # 가져온 episode list를 순회
            for episode in el:
                # 각 episode의 no가 recent_episode_no보다 클 경우,
                # self.episode_list에 추가
                if int(episode.no) > int(recent_episode_no):
                    new_list.append(episode)
                    self.webtoon.make_list_html(self.episode_list)
                    episode._make_html()
                    episode._save_images()
                    if int(episode.no) == 1:
                        break
                else:
                    break
            # break가 호출되지 않았을 때
            else:
                # 계속해서 진행해야 하므로 page값을 증가시키고 continue로 처음으로 돌아감
                page += 1
                continue
            # el의 for문에서 break가 호출될 경우(더 이상 추가할 episode없음
            # while문을 빠져나가기위해 break실행
            break
        self.episode_list = new_list + self.episode_list
        self.webtoon.make_list_html(self.episode_list)
        self.webtoon.save_thumbnail()
        self.save()
        return len(new_list)

    def get_last_page_episode_list(self):
        el = utils.get_webtoon_episode_list(self.webtoon, 99999)
        self.episode_list = el
        return len(self.episode_list)


    def save(self, path=None):
        """
        현재폴더를 기준으로 db/<webtoon_id>.txt 파일에
        pickle로 self.episode_list를 저장
        1. 폴더 생성시
            os.path.isdir('db')
                path가 directory인지
            os.mkdir(path)
                path의 디렉토리를 생성
        2. 저장시
            pickle.dump(obj, file)
                obj -> Object (모든 객체 가능)
                file -> File object (파일 객체, bytes형식으로 write가능한)
        :return: None(없음)
        """
        # db폴더가 있는지 검사
        if not os.path.isdir('db'):
            # 없으면 폴더 생성
            os.mkdir('db')

        obj = self.episode_list
        path = 'db/%s.txt' % self.webtoon.title_id
        pickle.dump(obj, open(path, 'wb'))
        self.save_webtoon_title()
    def load(self, path=None, init=False):
        """
        현재폴더를 기준으로 db/<webtoon_id>.txt 파일의 내용을 불러와
        pickle로 self.episode_list를 복원
        1. 만약 db폴더가 없으면 or db/webtoon_id.txt파일이 없으면
            -> "불러올 파일이 없습니다" 출력
        2. 있으면 복원
        :return: None(없음)
        """
        try:
            path = f'db/{self.webtoon.title_id}.txt'
            self.episode_list = pickle.load(open(path, 'rb'))
        except FileNotFoundError:
            if not init:
                print('파일이 없습니다')

    def save_webtoon_title(self):
        text = ""
        if os.path.isfile("webtoon/webtoon_title_id.txt"):
            text = open("webtoon/webtoon_title_id.txt", "rt").read()
        with open("webtoon/webtoon_title_id.txt", "a+") as f:
            if self.webtoon.title.replace(" ", "") not in text:
                f.write(f'{self.webtoon.title.replace(" ", "")} {self.webtoon.title_id} ')

    def load_webtoon_title(self):
        try:
            path = f'webtoon/webtoon_title_id.txt'
            webtoon_id_title_list = open("webtoon/webtoon_title_id.txt", "rt").read().split(" ")[:-1]
            self.webtoon_id_title_dict = dict(zip(webtoon_id_title_list[1::2], webtoon_id_title_list[::2]))
        except FileNotFoundError:
            print("파일이 없습니다")

if __name__ == '__main__':
    crawler = NaverWebtoonCrawler('르완')
    crawler.update_episode_list()
    crawler.load_webtoon_title()
    utils.make_index_html(crawler.webtoon_id_title_dict)
