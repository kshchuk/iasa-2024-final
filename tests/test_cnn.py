from web_scapper.cnn.cnn import CNNReader

def test_cnn_api():
    reader = CNNReader().build()
    data = reader.collect_recommended(keywords=["Shrek"], period="year")
    assert data
    assert len(data) == 5

    for t in data:
        assert len(t.content) > 100
