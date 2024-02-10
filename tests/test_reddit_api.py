from web_scapper.reddit.reddit import RedditReader
from web_scapper.search.post import Comment


def test_reddit_api():
    reader = RedditReader().build()
    data = reader.collect_data(keywords=["Israel", "Palestine", "War"], period="Year", post_limit=10, comment_limit=10)
    assert data
    assert data.source == 'Reddit'
    assert len(data.articles) == 10
    for article in data.articles:
        if len(article.comments) > 0:
            for comment in article.comments:
                assert isinstance(comment, Comment)
                assert len(comment.content)>0
