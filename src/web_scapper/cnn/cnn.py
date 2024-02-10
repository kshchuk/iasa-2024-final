import requests
from bs4 import BeautifulSoup
import json

from typing import List
from web_scapper.search.post import Article
from web_scapper.url_builder import CNNSearch
from web_scapper.search.common_search import SearchEngine


class CNNReader(SearchEngine):

    def build(self):
        return self

    def collect_recommended(self, keywords: List[str], period: str):
        return self.collect_data(keywords, period, 5, 0)

    def collect_data(self, keywords: List[str], period: str, post_limit=5, comment_limit=0) -> List[Article]:
        search_url = self._build_search_url(keywords, post_limit)
        articles = self.collect_links(search_url)
        return self._read_articles(articles)

    def _read_articles(self, articles_links):
        posts = []
        for link in articles_links:
            posts.append(self._collect_page_content(link))
        return posts

    def _build_search_url(self, keywords, post_limit):
        return CNNSearch.search(keywords, post_limit)

    def _collect_page_content(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._process_article_content(soup)
        else:
            raise RuntimeError(f"Failed to retrieve content from {url}, status code: {response.status_code}")

    def _process_article_content(self, soup):
        title_elem = soup.find('h1')
        title = self._to_plain_text(title_elem)
        h2s = self._to_plain_text_each(soup.find_all('h2'))
        ps = self._to_plain_text_each(soup.find_all('p'))
        content = " ".join(h2s + ps)
        return Article(title=title, content=content)

    def _to_plain_text(self, tag):
        if tag:
            return tag.get_text()
        else:
            return ""

    def _to_plain_text_each(self, tags):
        return [self._to_plain_text(tag) for tag in tags]

    def collect_links(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return self.process_response(data)

        else:
            print(f"Failed to retrieve JSON data from {url}, status code: {response.status_code}")

    def process_response(self, json_data):
        obj_data = json.loads(json_data) if isinstance(json_data, str) else json_data
        if obj_data.get('message') != 'success':
            raise ValueError('Received not successful response')
        links = []
        if isinstance(obj_data.get('result'), list):
            links = [item['path'] for item in obj_data['result'] if 'path' in item]
        else:
            raise ValueError("'result' is missing or is not a list")

        return links
