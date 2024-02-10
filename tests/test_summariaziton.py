import json

from src.response_parser.reddit_response_parser import RedditResponseParser
from src.nlp.ntlk.summarization import TF_IDFSummarizator


def test_summarization():
    summarizator = TF_IDFSummarizator()
    test_text_source = "assets/reddit/test_data/response-example.json"
    with open(test_text_source, "r") as file:
        response = file.read()
    response = RedditResponseParser.parse(json.loads(response))
    response_text = " ".join(response["data"])
    summary = summarizator.summarize(response_text, 20)
    print(summary)
    assert len(summary.split('.')) >= 20
