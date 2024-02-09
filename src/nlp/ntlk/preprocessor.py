import nltk
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('all')


class NTLKPreprocessor:
    def __init__(self, lemmatizer=WordNetLemmatizer(), stop_words=stopwords.words('english')):
        self._lemmatizer = lemmatizer
        self._stop_words = stop_words

    def preprocess_text(self, text: str) -> str:
        """ Preprocess a text by tokenizing, removing stop words, and lemmatizing the tokens"""
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        tokens = tokenizer.tokenize(text.lower())

        # tokens = word_tokenize(text.lower())
        filtered_tokens = [token for token in tokens if token not in self._stop_words]

        lemmatized_tokens = [self._lemmatizer.lemmatize(token) for token in filtered_tokens]

        # Join the tokens back into a string
        processed_text = ' '.join(lemmatized_tokens)

        return processed_text
