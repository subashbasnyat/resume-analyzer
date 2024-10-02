import nltk
from nltk import regexp_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


class TextCleaner:
    def __init__(self):
        # TODO: Download necessary NLTK data
        # nltk.download('punkt')
        # nltk.download('stopwords')
        # self.stop_words = set(stopwords.words('english'))
        pass

    def remove_stopwords(self, text):
        """
        Removes stop words (including capitalized ones) from the given string, if present.

        :param text: str: The string from which stop words will be removed.
        :returns: str: The cleaned string without stop words.

        """
        # check in lowercase
        t = [token for token in text if token.lower() not in stopwords.words("english")]
        text = " ".join(t)
        return text

    def remove_special_characters(self, text):
        # TODO: Implement special character removal
        """ "Function to remove special charactes"""

        # \w+ it matches alphanumeric characters and underscore
        pattern = r"\w+"

        # tokenizing the text based on the pattern
        tokens = regexp_tokenize(text, pattern)

        # Joining the token
        cleaned_tokens = " ".join(tokens)
        return cleaned_tokens

    def lowercase_text(self, text):
        # TODO: Implement text lowercasing
        # using lower() function to change the text into lower case
        return text.lower()

    def tokenize(self, text):
        words = []
        sentences = sent_tokenize(text)
        for each_sentence in sentences:
            n_words = word_tokenize(each_sentence)
            words.extend(n_words)
        return words

    def clean_text(self, text):
        # TODO: Implement the main cleaning method
        # This should call the other methods in the appropriate order
        lower_case = self.lowercase_text(text)
        remove_special_characters = self.remove_special_characters(lower_case)
        text_after_tokenization = self.tokenize(remove_special_characters)
        text_after_stopword_removal = self.remove_stopwords(text_after_tokenization)
        return text_after_stopword_removal


if __name__ == "__main__":
    # TODO: Add test code or example usage
    pass
