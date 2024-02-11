from typing import List
from web_analyzer.search.post import Article
from abc import ABC, abstractmethod


class SearchEngine(ABC):
    def build(self):
        return self

    @abstractmethod
    def collect_recommended(self, keywords: List[str], period: str):
        pass

    @abstractmethod
    def collect_data(self, keywords: List[str], period: str, post_limit=5, comment_limit=10) -> List[Article]:
        pass

    @staticmethod
    def period_to_days(period: str):
        d_map = {
            'Day': 1,
            'Week': 7,
            'Month': 31,
            'Year': 365
        }
        if period in d_map:
            return d_map[period]
        else:
            return 7
