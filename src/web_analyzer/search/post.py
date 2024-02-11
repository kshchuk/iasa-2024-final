
class Article:
    def __init__(self, title="", content="", votes=0, date_t=None, link='', comments=None):
        self.title = title
        self.content = content
        self.votes = votes
        if date_t:
            self.date = date_t
        else:
            self.date = None
        self.link = link
        if comments:
            self.comments = comments
        else:
            self.comments = []


class Comment:
    def __init__(self):
        self.content = ""
        self.votes = 0
        self.date_published = None


class ArticleCollection:
    def __init__(self, source=''):
        self.source = source
        self.articles = []

    def add(self, article: Article):
        self.articles.append(article)
