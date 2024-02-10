from nlp.ntlk.sentiment_analysis import NLTKSentimentAnalyzer
from nlp.ntlk.summarization import TF_IDFSummarizator
from nlp.utils.nlp_utils import SentimentType
from web_scapper.web_scraper import WebScraper
from pandas import DataFrame

sentence_number = 5


class Controller:
    def __init__(self, web_scrapper=WebScraper(),
                 sentiment_analyzer=NLTKSentimentAnalyzer(),
                 summarizer=TF_IDFSummarizator()
                 ):
        self._web_scrapper = web_scrapper
        self._sentiment_analyzer = sentiment_analyzer
        self._summarizer = summarizer

        self._current_dataframe: DataFrame = None

    def analyze_event(self, collection_data: dict):
        self._web_scrapper.build()

        article_collection = self._web_scrapper.collect_data(keywords=collection_data["tags"],
                                                             period=collection_data["timeperiod"],
                                                             services=collection_data["services"])
        # Initialize lists for each column
        titles = []
        summaries = []
        sentiments = []
        resources = []
        dates = []
        links = []

        for source in article_collection:

            for article in source.articles:
                article_content = [article.content]

                for comment in article.comments:
                    article_content.append(comment)

                content = ""
                for text in article_content:
                    content += text + ". "

                sentiment = self._sentiment_analyzer.get_sentiment(content)
                summary = self._summarizer.summarize(content, 5)

                # Append data to lists
                titles.append(article.title)
                summaries.append(summary)
                sentiments.append(
                    "1" if sentiment is SentimentType.POSITIVE
                    else "-1" if sentiment is SentimentType.NEGATIVE else "0")
                resources.append(source.source)
                dates.append(article.date)
                links.append(article.link)

        self._current_dataframe = DataFrame({
            "Title": titles,
            "Summary": summaries,
            "Sentiment": sentiments,
            "Resource": resources,
            "Date": dates,
            "Link": links
        })

        return self._current_dataframe

    def get_statistics(self):
        if self._current_dataframe is None:
            return "No data to analyze"

        # create trand 

controller = Controller()
