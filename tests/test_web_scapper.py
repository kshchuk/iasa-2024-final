from src.web_scapper.url_builder import RedditSearch


def test_reddit_url_builder():
    actual_url = RedditSearch.search(["Braid", "Anniversary", "Release"], "month")
    expected_url = 'https://www.reddit.com/search/?q=Braid+Anniversary+Release&type=link&t=month'
    assert actual_url == expected_url
