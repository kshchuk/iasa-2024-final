import json

from src.nlp.ntlk.topic_analysis import LDATopicAnalyzer
from src.response_parser.reddit_response_parser import RedditResponseParser


def test_topic_analysis():
    analyzer = LDATopicAnalyzer()
    test_text_source = "assets/reddit/test_data/response-example.json"
    with open(test_text_source, "r") as file:
        response = file.read()
    response = RedditResponseParser.parse(json.loads(response))
    analyzer.load(response["data"])
    topics = analyzer.fit(3)
    print(topics)
    analyzer.visualize_topics()
    assert len(topics) == 3


def test_topic_analysis_best_topic_number():
    analyzer = LDATopicAnalyzer()
    test_text_source = "assets/reddit/test_data/response-example.json"
    with open(test_text_source, "r") as file:
        response = file.read()
    response = RedditResponseParser.parse(json.loads(response))
    analyzer.load(response["data"])
    topics = analyzer.fit_best_topic_number(10, 2, 3)
    print(topics)
    analyzer.visualize_topics()
    # assert len(topics) == 3
