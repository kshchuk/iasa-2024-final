from nlp.ntlk.preprocessor import NTLKPreprocessor
from nlp.ntlk.sentiment_analysis import NLTKSentimentAnalyzer
from nlp.utils.nlp_utils import SentimentType


def test_sentiment_analysis():
    preprocessor = NTLKPreprocessor()
    analyzer = NLTKSentimentAnalyzer()

    text = "I love Biden"
    processed_text = preprocessor.preprocess_text(text)
    sentiment, _ = analyzer.get_sentiment(processed_text)

    assert sentiment == SentimentType.POSITIVE

    text = "I hate Trump"
    processed_text = preprocessor.preprocess_text(text)
    sentiment, _ = analyzer.get_sentiment(processed_text)

    assert sentiment == SentimentType.NEGATIVE

    text = "Thanks to everyone who joined and made today a great session! 🙌 nnIf weren't able to attend, we've got you covered. Academic researchers can now sign up for office hours for help using the new product track. See how you can sign up, here 👇nhttps://t.co/duIkd27lPx https://t.co/AP9YY4F8FG"
    processed_text = preprocessor.preprocess_text(text)
    sentiment, _ = analyzer.get_sentiment(processed_text)

    assert sentiment == SentimentType.POSITIVE

    text = "Quant industry is already extremely regulated. Labour in power won’t change anything."
    processed_text = preprocessor.preprocess_text(text)
    sentiment, _ = analyzer.get_sentiment(processed_text)

    assert sentiment == SentimentType.NEUTRAL
