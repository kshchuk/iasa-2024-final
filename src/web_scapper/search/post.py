from datetime import date


class ArticleCollection:
    def __init__(self):
        self.source = ''
        self.articles = []


class Article:
    def __init__(self, title="", content="", votes=0, comments=None):
        self.title = title
        self.content = content
        self.votes = votes
        self.date = date.today()
        self.link = ''
        if comments:
            self.comments = comments
        else:
            self.comments = []


class Comment:
    def __init__(self):
        self.content = ""
        self.votes = 0
