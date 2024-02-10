from web_scapper.web_scrapper import WebScrapper


def test_web_scrapper():
    web_scrapper = WebScrapper().build()
    article_collections = web_scrapper.collect_data(keywords=["Trump", "Biden"],
                                                    services=["Reddit", "CNN"], period="month")
    assert len(article_collections) == 2
    has_reddit = False
    has_cnn = False
    for article_collection in article_collections:
        if article_collection.source == 'Reddit':
            has_reddit = True
        elif article_collection.source == 'CNN':
            has_cnn = True
    assert has_reddit
    assert has_cnn
