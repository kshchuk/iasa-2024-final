from web_analyzer.cnn.cnn import CNNReader


def test_cnn_api():
    reader = CNNReader().build()
    data = reader.collect_data(keywords=["Shrek"], period="Year", post_limit=5)
    assert data
    assert len(data.articles) == 5
    assert data.source == 'CNN'
    for article in data.articles:
        assert len(article.content) > 100
        assert article.date
        assert article.link
