import os

import pyLDAvis.gensim
import pickle
import pyLDAvis

from gensim.models import LdaModel
from gensim.models import CoherenceModel
from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords

import gensim.corpora as corpora

from src.nlp.ntlk.preprocessor import NTLKPreprocessor


class LDATopicAnalyzer:
    def __init__(self, lemmatiser=WordNetLemmatizer(), stop_words=stopwords.words('english')):
        self._preprocessor = NTLKPreprocessor(lemmatiser, stop_words)
        self._num_topics = None
        self._texts = None
        self._lda_model = None
        self._id2word = None
        self._corpus = None

    def load(self, texts: list[str]) -> None:
        """
        Load the texts to analyze.

        :param texts: (list[str]) The list of texts to analyze
        """
        # list of words for each text
        processed_texts = [self._preprocessor.preprocess_text(text) for text in texts]
        processed_texts = [word_tokenize(text) for text in processed_texts if text != ""]

        self._id2word = corpora.Dictionary(processed_texts)

        # Term Document Frequency
        texts = processed_texts
        self._corpus = [self._id2word.doc2bow(text) for text in texts]
        self._texts = texts

    def fit(self, num_topics: int) -> list[tuple[int, list[tuple[str, float]]]]:
        """
        Fit the LDA model to the preprocessed texts.

        :param num_topics: (int) The number of topics to fit the model to

        :return: (list[tuple[int, list[tuple[str, float]]]]) The topics of the text.
        """
        # Alpha parameter is Dirichlet prior concentration parameter that represents document-topic density — with
        # a higher alpha, documents are assumed to be made up of more topics and result in more specific topic
        # distribution per document.
        #
        # Beta parameter is the same prior concentration parameter that represents topic-word density — with high
        # beta, topics are assumed to made of up most of the words and result in a more specific word distribution
        # per topic
        self._num_topics = num_topics
        self._lda_model = LdaModel(corpus=self._corpus,
                                   id2word=self._id2word,
                                   num_topics=num_topics,
                                   random_state=42,
                                   passes=10,
                                   alpha='auto',
                                   per_word_topics=True)

        return self._lda_model.print_topics()

    def fit_best_topic_number(self, limit: int, start: int = 2, step: int = 3) -> list[
        tuple[int, list[tuple[str, float]]]]:
        """
        Fit the LDA model to the preprocessed texts using the best number of topics.

        Can take a long time to run.

        :param limit: (int) Max num of topics
        :param start: (int) Min num of topics
        :param step: (int) Step between topics

        :return: (list[tuple[int, list[tuple[str, float]]]]) The topics of the text.
        """
        model_list, coherence_values = self._compute_coherence_values(limit, start, step)
        best_model = model_list[coherence_values.index(min(coherence_values))]
        self._lda_model = best_model
        topics = self._lda_model.print_topics()
        self._num_topics = len(topics)
        return topics

    def visualize_topics(self) -> None:
        """
        Visualize the topics of a text using the LDA algorithm

        :param topics: (list[tuple[int, list[tuple[str, float]]]]) The topics of the text
        """
        # pyLDAvis.enable_notebook()
        LDAvis_data_filepath = os.path.join('assets/results/ldavis_prepared_' + str(self._num_topics))

        LDAvis_prepared = pyLDAvis.gensim.prepare(self._lda_model, self._corpus, self._id2word)
        with open(LDAvis_data_filepath, 'wb') as f:
            pickle.dump(LDAvis_prepared, f)

        # load the pre-prepared pyLDAvis data from disk
        with open(LDAvis_data_filepath, 'rb') as f:
            LDAvis_prepared = pickle.load(f)
        pyLDAvis.save_html(LDAvis_prepared, 'assets/results/ldavis_prepared_' + str(self._num_topics) + '.html')

        # open the html file in a browser
        os.system('start ' + 'assets/results/ldavis_prepared_' + str(self._num_topics) + '.html')

    def _compute_coherence_values(self, limit, start=2, step=3):
        """
        Compute c_v coherence for various number of topics.

        Can take a long time to run.

        Topic coherence measures the degree of semantic similarity between high scoring words in a topic.
        It has been shown to correlate well with human interpretability of topics. You can compute topic coherence
        for different numbers of topics and choose the number that gives the highest coherence.

        :param limit: Max num of topics
        :param start: Min num of topics
        :param step: Step between topics

        :return: (model_list, coherence_values) List of LDA topic models and Coherence values
        corresponding to the LDA model with respective number of topics
        """
        coherence_values = []
        model_list = []
        for num_topics in range(start, limit, step):
            model = LdaModel(corpus=self._corpus,
                             id2word=self._id2word,
                             num_topics=num_topics,
                             random_state=42,
                             passes=10,
                             alpha='auto',
                             per_word_topics=True)
            model_list.append(model)
            coherencemodel = CoherenceModel(model=model, texts=self._texts, dictionary=self._id2word, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())

        return model_list, coherence_values
