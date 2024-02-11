from web_analyzer.youtube.youtube import YouTubeReader
from web_analyzer.reddit.reddit import RedditReader
from web_analyzer.cnn.cnn import CNNReader
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from web_analyzer.search.post import ArticleCollection


class WebScraper:

    def __init__(self):
        self.service_map = {}

    def build(self):
        self.service_map["YouTube"] = YouTubeReader().build()
        self.service_map["Reddit"] = RedditReader().build()
        self.service_map["CNN"] = CNNReader().build()
        return self

    def collect_data(self, keywords: List[str], services: List[str], period: str) -> List[ArticleCollection]:
        collections = []
        futures = []

        with ThreadPoolExecutor(max_workers=len(services)) as executor:
            for service in services:
                try:
                    service_obj = self.service_map[service]
                    future = executor.submit(service_obj.collect_recommended, keywords, period)
                    futures.append(future)
                except Exception as e:
                    print(f"An error occurred: {e}")

            for future in as_completed(futures):
                try:
                    article_collection = future.result()
                    collections.append(article_collection)
                except Exception as e:
                    print(f"An error occurred: {e}")

        return collections
