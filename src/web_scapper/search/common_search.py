from typing import List
from web_scapper.search.post import Article


class SearchEngine:
    def build(self):
        return self

    def collect_recommended(self, keywords: List[str], period: str):
        pass

    def collect_data(self, keywords: List[str], period: str, post_limit=5, comment_limit=10) -> List[Article]:
        pass

    @staticmethod
    def period_to_days(period: str):
        d_map = {
            'day': 1,
            'week': 7,
            'month': 31,
            'year': 365
        }
        if period in d_map:
            return d_map[period]
        else:
            return 7
