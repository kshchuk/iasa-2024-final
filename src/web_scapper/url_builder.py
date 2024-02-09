from typing import List


class RedditSearch:
    @staticmethod
    def search(keywords: List[str], time="month"):
        return RedditUrlBuilder().search().append_keywords(keywords).and_with().has_type().and_with().time(time).get()


class RedditUrlBuilder:

    def __init__(self, base=None):
        if base:
            self._url = base
        else:
            self._url = 'https://www.reddit.com/'

    def search(self):
        self._url = self._url + 'search/?'
        return self

    def append_keywords(self, keywords):
        self._url = self._url + 'q='
        output_string = "+".join(keywords)
        self._url = self._url + output_string
        return self

    def and_with(self):
        self._url = self._url + '&'
        return self

    def has_type(self, d_type='link'):
        self._url = self._url + f'type={d_type}'
        return self

    def time(self, d_time='month'):
        self._url = self._url + f't={d_time}'
        return self

    def get(self):
        return self._url
