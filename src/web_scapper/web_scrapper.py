from web_scapper.youtube.youtube import YouTubeReader
from web_scapper.reddit.reddit import RedditReader
from web_scapper.cnn.cnn import CNNReader
from typing import List
from search.post import ArticleCollection


class WebScrapper:

    def __init__(self):
        self.service_map = {}

    def build(self):
        self.service_map["YouTube"] = YouTubeReader().build()
        self.service_map["Reddit"] = RedditReader().build()
        self.service_map["CNN"] = CNNReader().build()

    def collect_data(self, keywords: List[str], services: List[str], period: str) -> [ArticleCollection]:
        collections = []
        for service in services:
            service = self.service_map[service]
            article_collection = service.collect_recommended(keywords, period)
            collections.append(article_collection)
        return collections
