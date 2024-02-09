import praw.models
import environment.env_variables as env
from typing import List
from web_scapper.search.post import Article
from web_scapper.search.post import Comment


class RedditReader:

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

    def collect_data(self, keywords: List[str], period: str, post_limit=10, comment_limit=10) -> List[Article]:
        all_subreddits = self.reddit.subreddit("all")
        search_tag = ", ".join(keywords)

        posts = []
        if post_limit < 1:
            return posts
        for submission in all_subreddits.search(search_tag, limit=post_limit, time_filter=period):
            title = submission.title
            score = submission.score
            text = submission.selftext
            post = Article(title=title, content=text, votes=score)
            submission.comments.replace_more(limit=0)
            posts.append(post)
            comments = []
            post.comments = comments
            if comment_limit < 1:
                continue
            for comment in submission.comments.list()[:comment_limit]:
                new_comment = Comment()
                new_comment.content = comment.body
                new_comment.votes = comment.score
                comments.append(comment)

        return posts
