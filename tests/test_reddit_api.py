from web_scapper.reddit.reddit import RedditReader


def test_reddit_api():
    reader = RedditReader().build()
    data = reader.collect_data(keywords=["Israel", "Palestine", "War"], period="year", post_limit=10, comment_limit=0)
    assert data
    assert len(data) == 10
