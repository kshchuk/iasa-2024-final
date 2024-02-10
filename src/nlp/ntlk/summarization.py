import math

from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords

from nlp.ntlk.preprocessor import NTLKPreprocessor

threshold_coeff = 1.6


class TF_IDFSummarizator:
    """Summarize a text using the TF-IDF algorithm"""

    def __init__(self, lemmatiser=WordNetLemmatizer(), stop_words=stopwords.words('english')):
        self._preprocessor = NTLKPreprocessor(lemmatiser, stop_words)

    def summarize(self, text: str, num_sentences: int) -> str:
        """
        Summarize a text using the TF-IDF algorithm

        :param text: (list[str]) The list of text to summarize
        :param num_sentences: The number of sentences to include in the summary
        :return: (str) The summary of the text
        """
        sentences = text.split(".")
        sentences = [sentence for sentence in sentences if len(sentence) > 1]

        frequency_matrix = self._create_frequency_matrix(sentences)  # Frequency of words in each sentence

        # Number of times term appears in a document / Total number of terms in the document
        tf_matrix = self._create_tf_matrix(frequency_matrix)

        # Number of sentences in which a word appears
        count_doc_per_words = self._create_documents_per_words(frequency_matrix)

        # log_e(Total number of documents / Number of documents with term t in it)
        idf_matrix = self._create_idf_matrix(frequency_matrix, count_doc_per_words, len(sentences))

        # TF-IDF algorithm is made of 2 algorithms multiplied together.
        tf_idf_matrix = self._create_tf_idf_matrix(tf_matrix, idf_matrix)

        # Score a sentence by its word's TF
        sentence_scores = self._score_sentences(tf_idf_matrix)

        # Find the average score from the sentence value dictionary
        threshold = self._find_average_score(sentence_scores) * threshold_coeff

        # determine the threshold to include exactly num_sentences in the summary
        summary = self._generate_summary(sentences, sentence_scores, threshold)
        summary_sentences = summary.split(".")
        summary_sentences = [sentence for sentence in summary_sentences if len(sentence) > 1]
#        while len(summary_sentences) > num_sentences:
#            threshold += 0.1
#            summary = self._generate_summary(sentences, sentence_scores, threshold)
#            summary_sentences = summary.split(".")
#            summary_sentences = [sentence for sentence in summary_sentences if len(sentence) > 1]

#        while len(summary_sentences) < num_sentences:
#            threshold -= 0.05
#            summary = self._generate_summary(sentences, sentence_scores, threshold)
#            summary_sentences = summary.split(".")
#            summary_sentences = [sentence for sentence in summary_sentences if len(sentence) > 1]

        print(f"Summary length: {len(summary_sentences)}")
        #if len(summary_sentences) > num_sentences:
        #    summary_sentences = summary_sentences[:num_sentences]

        summary = ""
        for sentence in summary_sentences: summary += sentence + "."
        return summary

    def _create_frequency_matrix(self, sentences: list[str]) -> dict[str, dict[str, int]]:
        """
        Calculates the frequency of words in each sentence

        :param sentences:
        :return: (dict) Sentence is the key and the value is a dictionary of word frequency.
        """
        frequency_matrix = {}

        for sent in sentences:
            freq_table = {}

            preprocessed_sent = self._preprocessor.preprocess_text(sent)
            words = word_tokenize(preprocessed_sent)

            for word in words:
                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1

            frequency_matrix[sent[:15]] = freq_table

        return frequency_matrix

    @staticmethod
    def _create_tf_matrix(freq_matrix) -> dict[str, dict[str, float]]:
        """Calculates TF(t) = (Number of times term t appears in a document) /
        / (Total number of terms in the document)"""
        tf_matrix = {}

        for sent, f_table in freq_matrix.items():
            tf_table = {}

            count_words_in_sentence = len(f_table)
            for word, count in f_table.items():
                tf_table[word] = count / count_words_in_sentence

            tf_matrix[sent] = tf_table

        return tf_matrix

    @staticmethod
    def _create_documents_per_words(freq_matrix) -> dict[str, int]:
        """Returns a dictionary with the number of documents in which a word appears"""
        word_per_doc_table = {}

        for sent, f_table in freq_matrix.items():
            for word, count in f_table.items():
                if word in word_per_doc_table:
                    word_per_doc_table[word] += 1
                else:
                    word_per_doc_table[word] = 1

        return word_per_doc_table

    @staticmethod
    def _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents) -> dict[str, dict[str, float]]:
        """Calculates IDF(t) = log_e(Total number of documents / Number of documents with term t in it)"""

        idf_matrix = {}

        for sent, f_table in freq_matrix.items():
            idf_table = {}

            for word in f_table.keys():
                idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

            idf_matrix[sent] = idf_table

        return idf_matrix

    @staticmethod
    def _create_tf_idf_matrix(tf_matrix, idf_matrix) -> dict[str, dict[str, float]]:
        """TF-IDF algorithm is made of 2 algorithms multiplied together.

        In simple terms, we are multiplying the values from both the matrix and generating new matrix.
        """
        tf_idf_matrix = {}

        for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

            tf_idf_table = {}

            for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                        f_table2.items()):  # here, keys are the same in both the table
                tf_idf_table[word1] = float(value1 * value2)

            tf_idf_matrix[sent1] = tf_idf_table

        return tf_idf_matrix

    @staticmethod
    def _score_sentences(tf_idf_matrix) -> dict:
        """ Score a sentence by its word's TF
        Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
        :rtype: dict
        """

        sentenceValue = {}

        for sent, f_table in tf_idf_matrix.items():
            total_score_per_sentence = 0

            count_words_in_sentence = len(f_table)
            for word, score in f_table.items():
                total_score_per_sentence += score

            if count_words_in_sentence != 0:
                sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence

        return sentenceValue

    @staticmethod
    def _find_average_score(sentenceValue) -> float:
        """
        Find the average score from the sentence value dictionary

        :rtype: float
        """

#        if len(sentenceValue) == 0:
#            return 0

        sumValues = 0
        for entry in sentenceValue:
            sumValues += sentenceValue[entry]

        # Average value of a sentence from original summary_text
        average = (sumValues / len(sentenceValue))

        return average

    @staticmethod
    def _generate_summary(sentences, sentence_value, threshold: float) -> str:
        """
        Selects a sentence for a summarization if the sentence score is more than the average score

        :param sentences: The sentences to summarize
        :param sentence_value: The values of the sentences
        :param threshold: (float) The threshold to use for the sentence value to be included in the summary
        """
        sentence_count = 0
        summary = ''

        for sentence in sentences:
            if sentence[:15] in sentence_value and sentence_value[sentence[:15]] >= threshold:
                summary += "." + sentence
                sentence_count += 1

        return summary
