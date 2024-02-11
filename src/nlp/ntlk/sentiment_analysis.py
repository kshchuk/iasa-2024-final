import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from nlp.utils.nlp_utils import SentimentType

nltk.download('all')


class NLTKSentimentAnalyzer:
    def __init__(self):
        self._analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(self, text: str) -> (SentimentType, float):
        """
        Get the sentiment of a text

        :param text: The text to analyze
        :return: (SentimentType) The sentiment of the text. One of POSITIVE, NEGATIVE, NEUTRAL
        """
        scores = self._analyzer.polarity_scores(text)

        if scores['compound'] >= 0.05:
            return SentimentType.POSITIVE, scores['compound']
        elif scores['compound'] <= -0.05:
            return SentimentType.NEGATIVE, scores['compound']
        else:
            return SentimentType.NEUTRAL, scores['compound']
