import datetime

from web_scapper.youtube.youtube import YouTubeReader


def test_youtube_api():
    reader = YouTubeReader().build()
    data = reader.collect_data(keywords=["Shrek"], period="Year", post_limit=5, comment_limit=10)
    assert data
    assert len(data.articles) == 5
    assert data.source == 'YouTube'
    for article in data.articles:
        assert article.link != ''
        assert article.date < datetime.datetime.now()
        assert article.votes >= 0
        assert article.title
        assert article.title != ''

