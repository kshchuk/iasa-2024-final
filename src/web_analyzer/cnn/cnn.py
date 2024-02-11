import requests
from bs4 import BeautifulSoup
import json

from typing import List
from web_analyzer.search.post import Article
from web_analyzer.search.post import ArticleCollection
from web_analyzer.url_builder import CNNSearch
from web_analyzer.search.common_search import SearchEngine
from datetime import datetime, timedelta


class CNNReader(SearchEngine):

    def build(self):
        return self

    def collect_recommended(self, keywords: List[str], period: str):
        period_to_limit = {
            "Day": 5,
            "Week": 10,
            "Month": 15,
            "Year": 20
        }
        post_limit = 10
        if period in period_to_limit:
            post_limit = period_to_limit[period]
        return self.collect_data(keywords, period, post_limit, 0)

    def collect_data(self, keywords: List[str], period: str, post_limit=5, comment_limit=0) -> ArticleCollection:
        search_url = self._build_search_url(keywords, post_limit)
        articles = self.collect_links(search_url)
        return self._read_articles(articles, period)

    def _read_articles(self, articles_links, period):
        posts = ArticleCollection('CNN')
        period_days = SearchEngine.period_to_days(period)
        for link in articles_links:
            article = self._collect_page_content(link)
            if article.date:
                if datetime.now() - timedelta(days=period_days) > article.date:
                    continue
                posts.add(article)
        return posts

    def _build_search_url(self, keywords, post_limit):
        return CNNSearch.search(keywords, post_limit)

    def _collect_page_content(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._process_article_content(soup, url)
        else:
            raise RuntimeError(f"Failed to retrieve content from {url}, status code: {response.status_code}")

    def _process_article_content(self, soup, link):
        title_elem = soup.find('h1')
        title = self._to_plain_text(title_elem)
        h2s = self._to_plain_text_each(soup.select('article h2'))
        ps = self._to_plain_text_each(soup.select('article p'))
        content = " ".join(h2s + ps)
        date_obj = self._extract_date(soup)
        return Article(title=title, content=content, date_t=date_obj, link=link)

    def _extract_date(self, soup):
        meta_tag = soup.find('meta', attrs={'name': 'pubdate'})
        date_str = meta_tag['content'] if meta_tag else None
        if date_str:
            return datetime.fromisoformat(date_str.rstrip('Z'))
        else:
            meta_tag = soup.find('meta', property="article:published_time")
            date_str = meta_tag['content'] if meta_tag else None
            if date_str:
                return datetime.fromisoformat(date_str.rstrip('Z'))
            return None

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
