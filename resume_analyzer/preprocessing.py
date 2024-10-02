import nltk
from nltk import regexp_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class TextCleaner:
    def __init__(self):
        # TODO: Download necessary NLTK data
        # nltk.download('punkt')
        # nltk.download('stopwords')
        # self.stop_words = set(stopwords.words('english'))
        pass

    def remove_stopwords(self, text):
        # TODO: Implement stopword removal using self.stop_words
        pass

    def remove_special_characters(self, text):
        # TODO: Implement special character removal
        """"Function to remove special charactes"""

        # \w+ it matches alphanumeric characters and underscore
        pattern = r'\w+'

        #tokenizing the text based on the pattern
        tokens = regexp_tokenize(text, pattern)

        #Joining the token
        cleaned_tokens = ' '.join(tokens)
        return cleaned_tokens
        pass

    def remove_punctuation(self, text):
        # TODO: Implement punctuation removal
        pass

    def lowercase_text(self, text):
        # TODO: Implement text lowercasing
        #using lower() function to change the text into lower case
        return text.lower()
        pass

    def tokenize(self, text):
        # TODO: Implement tokenization using NLTK's word_tokenize
        pass

    def clean_text(self, text):
        # TODO: Implement the main cleaning method
        # This should call the other methods in the appropriate order
        print("Text for Cleaning: ", text)
        return "Not implemented"

if __name__ == "__main__":
    # TODO: Add test code or example usage
    pass
