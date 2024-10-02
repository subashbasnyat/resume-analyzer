import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize


class TextCleaner:
    """ """

    def __init__(self):
        # TODO: Download necessary NLTK data
        # nltk.download('punkt')
        # nltk.download('stopwords')
        # self.stop_words = set(stopwords.words('english'))
        pass

    def remove_stopwords(self, text):
        """Removes stop words (including capitalized ones) from the given string, if present.

        :param text: str: The string from which stop words will be removed.
        :returns: str: The cleaned string without stop words.

        """
        # check in lowercase
        t = [
            token for token in text
            if token.lower() not in stopwords.words("english")
        ]
        text = " ".join(t)
        return text

    def remove_special_characters(self, text):
        """

        :param text:

        """
        # TODO: Implement special character removal
        pass

    def remove_punctuation(self, text):
        """

        :param text:

        """
        # TODO: Implement punctuation removal
        pass

    def lowercase_text(self, text):
        """

        :param text:

        """
        # TODO: Implement text lowercasing
        pass

    def tokenize(self, text):
        """

        :param text:

        """
        words = []
        sentences = sent_tokenize(text)
        for each_sentence in sentences:
            n_words = word_tokenize(each_sentence)
            words.extend(n_words)
        return words

    def clean_text(self, text):
        """

        :param text:

        """
        # TODO: Implement the main cleaning method
        # This should call the other methods in the appropriate order
        text_after_tokenization = self.tokenize(text)
        text_after_stopword_removal = self.remove_stopwords(
            text_after_tokenization)
        return text_after_stopword_removal


if __name__ == "__main__":
    # TODO: Add test code or example usage
    pass
