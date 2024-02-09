from web_scapper.youtube.youtube import YouTubeReader


def test_youtube_api():
    reader = YouTubeReader().build()
    data = reader.collect_recommended(keywords=["Shrek"], period="year")
    assert data
    assert len(data) == 5
