import re
import unicodedata

from bs4 import BeautifulSoup
import spacy
from spacy.lang.en import English
import contractions
from datetime import datetime
from spacy.cli import download


try:
    spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")

class TextCleaner:
    """A class for cleaning and processing text data."""

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.tokenizer = English().tokenizer

    def lowercase_text(self, text):
        """Converts the given text to lowercase.

        :param text: str: The string to be converted to lowercase.
        :returns: str: The lowercased string.

        """
        return text.lower()

    def remove_html_tags_func(self, text):
        """Removes HTML-Tags from a string, if present.

        :param text: str: The string from which HTML tags will be removed.
        :returns: str: The cleaned string without HTML tags.

        """
        return BeautifulSoup(text, "html.parser").get_text()

    def remove_accented_chars_func(self, text):
        """Removes all accented characters from a string, if present.

        :param text: str: The string from which accented characters will be removed.
        :returns: str: The cleaned string without accented characters.

        """
        return (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("utf-8", "ignore")
        )

    def remove_punctuation_func(self, text):
        """Removes all punctuation from a string.

        :param text: str: The string from which punctuation will be removed.
        :returns: str: The cleaned string without punctuation.

        """
        return re.sub(r"[^a-zA-Z0-9]", " ", text)

    def remove_extra_whitespaces_func(self, text):
        """Removes extra whitespaces from a string, if present.

        :param text: str: The string from which extra whitespaces will be removed.
        :returns: str: The cleaned string without extra whitespaces.

        """
        return re.sub(r"^\s*|\s\s*", " ", text).strip()

    def remove_stopwords(self, text):
        """Removes stop words (including capitalized ones) from the given string.

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

    def expand_contractions(self, text):
        """Expands contractions in the given text.

        :param text: str: The string where contractions will be expanded.
        :returns: str: The string with expanded contractions.

        """
        return contractions.fix(text)

    def tokenize(self, text):
        """Tokenizes the given text using spaCy.

        :param text: str: The string to be tokenized.
        :returns: list: A list of token strings.

        """
        doc = self.tokenizer(text)
        return [token.text for token in doc]
    

    def remove_irr_char_func(self, text):
        """Removes all irrelevant characters (numbers and punctuation) from a string, if present
        
        :param text: str: String to which the function is to be applied, string
        :returns: list: Clean string without irrelevant characters
        """

        return re.sub(r'[^a-zA-Z]', ' ', text)

    def clean_text(self, text):
        """Applies all cleaning steps to the given text.

        :param text: str: The string to be cleaned.
        :returns: list: A list of cleaned and tokenized words.

        """
        lowercased = self.lowercase_text(text)
        irrelevant_removed = self.remove_irr_char_func(lowercased)
        expanded = self.expand_contractions(irrelevant_removed)
        no_html = self.remove_html_tags_func(expanded)
        no_accented_chars = self.remove_accented_chars_func(no_html)
        no_punct = self.remove_punctuation_func(no_accented_chars)
        no_extra_whitespaces = self.remove_extra_whitespaces_func(no_punct)
        no_stopwords = self.remove_stopwords(no_extra_whitespaces)
        tokenized = self.tokenize(no_stopwords)
        return tokenized

if __name__ == "__main__":
    cleaner = TextCleaner()
    sample_text = '''
    This is an example sentence! It includes contractions (e.g., can't, won't), 
    accented characters (é, ñ, ü), 
    <html>tags</html>, 
    punctuation!!!, 
    and stopwords like "is," "an," and "the." 
    Let's clean this up.
    '''
    print(cleaner.clean_text(text = sample_text))
