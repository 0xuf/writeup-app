from requests import get
from bs4 import BeautifulSoup


class MediumScrapper:
    medium_url = "https://medium.com/{}"
    output_data = []
    BASE_URL = "https://medium.com/tag/{}/latest"
    headers = {
        'Host': 'medium.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
    }

    def __init__(self, tag: str) -> None:
        """
        :param tag: receives the information based on the tag parameter
        """
        self.tag = tag
        self.BASE_URL = self.BASE_URL.format(tag)

    def get_response(self) -> list:
        """
        This method receives the posts and outputs them as a list
        :return: all_posts
        """
        _resp = get(url=self.BASE_URL, headers=self.headers)
        bs = BeautifulSoup(_resp.content.decode('utf-8'), 'html.parser')
        all_posts = bs.findAll("div", class_="kj kk kl l")
        for post in all_posts:
            _author = dict(
                name=post.findNext(
                    "p",
                    class_="bn b bo bp fm kr hd he hf hg fy hh gg"
                ).text,
                username=self.medium_url.format(post.findNext(
                    "a",
                    class_="au av aw ax ay az ba bb bc bd be bf bg bh bi"
                ).attrs['href'].split("?")[0].replace("/", "")
                                                ))
            _post = dict(
                title=post.findNext(
                    "h2",
                    class_="bn gi lf lg lh li gm lj lk ll lm gq ln lo lp lq gu lr ls "
                           "lt lu gy lv lw lx ly hc fm hd he hg hh gg"
                ).text,
                link=self.medium_url.format(post.findNext(
                    "a",
                    {"aria-label": "Post Preview Title"}
                ).attrs['href'].split("?")[0].replace("/", "")
                                            ))

            self.output_data.append(
                {
                    'author': _author,
                    'post': _post
                }
            )

        return self.output_data
