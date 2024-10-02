import re
import unicodedata

import spacy
from spacy.lang.en import English


class TextCleaner:
    """A class for cleaning and processing text data."""

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.tokenizer = English().tokenizer

    def remove_stopwords(self, text):
        """Removes stop words (including capitalized ones) from the given string, if present.

        :param text: str: The string from which stop words will be removed.
        :returns: str: The cleaned string without stop words.

        """
        doc = self.nlp(text)
        tokens = [token.text for token in doc if not token.is_stop]
        return " ".join(tokens)

    def remove_special_characters(self, text):
        """Removes special characters from the given string.

        :param text: str: The string from which special characters will be removed.
        :returns: str: The cleaned string without special characters.

        """
        pattern = r"\w+"
        tokens = re.findall(pattern, text)
        return " ".join(tokens)

    def lowercase_text(self, text):
        """Converts the given text to lowercase.

        :param text: str: The string to be converted to lowercase.
        :returns: str: The lowercased string.

        """
        return text.lower()

    def tokenize(self, text):
        """Tokenizes the given text using spaCy.

        :param text: str: The string to be tokenized.
        :returns: list: A list of token strings.

        """
        doc = self.tokenizer(text)
        return [token.text for token in doc]

    def remove_accented_chars_func(self, text):
        """Removes all accented characters from a string, if present

        :param text: String to which the function is to be applied, string
        :type text: str
        :returns: Clean string without accented characters

        """

        return (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("utf-8", "ignore")
        )

    def clean_text(self, text):
        """Applies all cleaning steps to the given text.

        :param text: str: The string to be cleaned.
        :returns: list: A list of cleaned and tokenized words.

        """
        lowercased = self.lowercase_text(text)
        remove_accented = self.remove_accented_chars_func(lowercased)
        no_special_chars = self.remove_special_characters(remove_accented)
        no_stopwords = self.remove_stopwords(no_special_chars)
        tokenized = self.tokenize(no_stopwords)
        return tokenized


if __name__ == "__main__":
    # TODO: Add test code or example usage
    pass
