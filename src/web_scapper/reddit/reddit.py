import praw.models
import environment.env_variables as env
from typing import List
from web_scapper.search.post import Article
from web_scapper.search.post import ArticleCollection
from web_scapper.search.post import Comment
from web_scapper.search.common_search import SearchEngine
from datetime import datetime


class RedditReader(SearchEngine):

    def __init__(self):
        self.reddit = None

    def build(self):
        user_id = env.Environment.reddit_user_id()
        assert user_id

        secret = env.Environment.reddit_user_secret()
        assert secret
        self.reddit = praw.Reddit(
            client_id=user_id,
            client_secret=secret,
            user_agent="Agent",
        )
        return self

    def collect_recommended(self, keywords: List[str], period: str):
        return self.collect_data(keywords, period)

    def collect_data(self, keywords: List[str], period: str, post_limit=10, comment_limit=10) -> ArticleCollection:
        all_subreddits = self.reddit.subreddit("all")
        search_tag = ", ".join(keywords)

        posts = ArticleCollection(source='Reddit')
        if post_limit < 1:
            return posts
        for submission in all_subreddits.search(search_tag, limit=post_limit, time_filter=period.lower()):
            title = submission.title
            score = submission.score
            text = submission.selftext
            created_time = submission.created
            date_obj = datetime.fromtimestamp(created_time)
            link = 'https://www.reddit.com' + submission.permalink
            post = Article(title=title, content=text, votes=score, link=link, date_t=date_obj)
            submission.comments.replace_more(limit=0)
            posts.add(post)
            comments = []
            if comment_limit < 1:
                continue
            for comment in submission.comments.list()[:comment_limit]:
                new_comment = Comment()
                new_comment.content = comment.body
                new_comment.votes = comment.score
                new_comment.date_published = datetime.fromtimestamp(comment.created_utc)
                comments.append(new_comment)
            post.comments = comments

        return posts
