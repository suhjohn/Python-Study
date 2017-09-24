# Webtoon = namedtuple('Webtoon', ['title_id', 'img_url', 'title'])

from bs4 import BeautifulSoup
import requests
import os


class Webtoon:
    def __init__(self, title_id, img_url, title):
        self._title_id = title_id
        self._img_url = img_url
        self._title = title
        self._description = None
        self.thumbnail_dir = f'webtoon/{self.title_id}/_thumbnail'

    @property
    def title_id(self):
        return self._title_id

    @property
    def img_url(self):
        return self._img_url

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    def get_description(self):
        webtoon_list_url = 'http://comic.naver.com/webtoon/list.nhn'
        params = {
            'titleId': self.title_id,
        }
        response = requests.get(webtoon_list_url, params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        description = soup.select("div.detail")[0].p
        return description

    def save_thumbnail(self):
        response = requests.get(self.img_url)
        with open(f'{self.thumbnail_dir}/{self.title_id}_thumbnail.jpg', 'wb') as f:
            f.write(response.content)

    def make_list_html(self, episode_list):
        """
        self.episode_list를 HTML파일로 만들어준다
        webtoon/{webtoon_id}.html
        1. webtoon폴더 있는지 검사 후 생성
        2. webtoon/{webtoon_id}.html 파일객체 할당 또는 with문으로 open
        3. open한 파일에 HTML앞부분 작성
        4. episode_list를 for문돌며 <tr>...</tr>부분 반복작성
        5. HTML뒷부분 작성
        6. 파일닫기 또는 with문 빠져나가기
        7. 해당파일 경로 리턴
        """
        """
        ex)
        <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body>
            <table>
                <!-- 이부분을 episode_list의 길이만큼 반복 -->
                <tr>
                    <td><img src="...."></td>
                    <td>제목</td>
                    <td>별점</td>
                    <td>날짜</td>
                </tr>
            </table>
        </body>
        </html>
        :return: 파일의 경로
        """
        # webtoon/ 폴더 존재하는지 확인 후 없으면 생성
        if not os.path.isdir(f'webtoon/{self.title_id}/html'):
            os.mkdir(f'webtoon/{self.title_id}/html')
        filename = f'webtoon/{self.title_id}/html/{self.title_id}.html'
        with open(filename, 'wt') as f:
            # HTML HEAD
            list_html_head = open('html/head.html', 'rt').read()
            f.write(list_html_head)

            # HTML NAVBAR
            navbar = open('html/navibar.html', 'rt').read()
            f.write(navbar.format(
                index_page=f'../../index.html'
            ))
            # INDEX PAGE TOP
            list_html_list_top = open('html/list_html_list_top.html', 'rt').read()
            f.write(list_html_list_top.format(
                title=f'{self.title}'
            ))
            # HTML EPISODE
            for e in episode_list:
                list_html_tr = open('html/list_html_tr.html', 'rt').read()
                f.write(list_html_tr.format(
                    episode_link=f'Episode_{e.no}.html',
                    img_url=f'../_thumbnail/{e.no}.jpg',
                    title=e.title,
                    rating=e.rating,
                    created_date=e.created_date
                ))
            # HTML 뒷부분 작성
            list_html_tail = open('html/list_html_tail.html', 'rt').read()
            f.write(list_html_tail)
        return filename

