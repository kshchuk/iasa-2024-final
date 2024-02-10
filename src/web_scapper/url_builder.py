from typing import List
from uuid import uuid4
import re


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


class CNNSearch:
    @staticmethod
    def search(keywords: List[str], post_limit: int):
        return (CNNUrlBuilder().search().append_keywords(keywords).and_with().size(post_limit).and_with()
                .append_pagination().and_with().with_sort('newest').and_with().has_type('article').and_with()
                .append_request_id().get())


class CNNUrlBuilder:

    def __init__(self, base=None):
        if base:
            self._url = base
        else:
            self._url = 'https://search.prod.di.api.cnn.io'

    def search(self):
        self._url = self._url + '/content?'
        return self

    def append_keywords(self, keywords):
        self._url = self._url + 'q='
        keywords = self._format_words(keywords)
        output_string = "+".join(keywords)
        self._url = self._url + output_string
        return self

    def _format_words(self, keywords):
        actual = []
        for word in keywords:
            word = self._modify_word(word)
            actual.append(word)
        return actual

    def _modify_word(self, word):
        word = re.sub(r'\s+', ' ', word)
        word = word.strip()
        word = word.replace(' ', '+')
        return word

    def and_with(self):
        self._url = self._url + '&'
        return self

    def has_type(self, d_type='article'):
        self._url = self._url + f'types={d_type}'
        return self

    def append_request_id(self):
        self._url = self._url + f'request_id={self._generate_request_id()}'
        return self

    def append_pagination(self, from_p=0, page_n=1):
        self._url = self._url + f'from={from_p}&page={page_n}'
        return self

    def with_sort(self, sorting='newest'):
        self._url = self._url + f'sort={sorting}'
        return self

    def size(self, size=10):
        self._url = self._url + f'size={size}'
        return self

    def _generate_request_id(self):
        uuid = uuid4()
        request_id = f"pdx-search-{uuid}"
        return request_id

    def get(self):
        return self._url

# https://search.prod.di.api.cnn.io/content?q=&size=10&from=0&page=1&sort=newest&types=article&request_id=pdx-search-b0d19b6a-46be-4742-8139-515df9eabc39
