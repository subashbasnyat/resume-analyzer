import re
import unicodedata
from datetime import datetime

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

        return (unicodedata.normalize("NFKD",
                                      text).encode("ascii", "ignore").decode(
                                          "utf-8", "ignore"))

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

    def extract_contact_info(self, text):
        # regex for email extraction
        email = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        
        # regex for phone number extraction to cover different formats
        phone = re.findall(r'\+?\d{1,4}?[\s.-]?\(?\d{1,4}?\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,9}', text)
        
        # regex for LinkedIn URLs
        linkedin = re.findall(r'linkedin\.com\/[a-zA-Z0-9\-_\/]+', text)
        
        # Regex to extract years of experience
        experience = re.findall(r'(\d+)\s*(?:year|years|yrs)\s*(?:of)?\s*(?:experience)?', text.lower())
        
        return {
            'email': email[0] if email else None,
            'phone': phone[0] if phone else None,
            'linkedin': linkedin[0] if linkedin else None,
            'years_of_experience': experience if experience else None
        }

       # contact_info = {filename: extract_contact_info(text) for filename, text in preprocessed_resumes.items()}
    
    def extract_experience(self, text):
        # Regex pattern to capture role, company, location, and date range
        #pattern = r'(?P<role>[\w\s]+)\s*-\s*(?P<company>[\w\s&]+)\s*-\s*(?P<location>[\w\s,]+)\s*(?P<start_date>\w+\s+\d{4})\s*-\s*(?P<end_date>\w+\s+\d{4}|Present)'
        pattern = r'(?P<company>[A-Z\s.,&]+)\n(?P<role>[\w\s]+)\s*\|\s*(?P<start_date>\w+\s+\d{4})\s*–\s*(?P<end_date>\w+\s+\d{4}|Present)'

        matches = re.findall(pattern, text)
        experiences = []

        for match in matches:
            #role, company, location, start_date, end_date = match
            
            #role, location, start_date, end_date = match
            company = match.group('company').strip()
            role = match.group('role').strip()
            start_date = match.group('start_date').strip()
            end_date = match.group('end_date').strip()
                    
            print(company)
            # Parse the start and end dates to calculate years of experience
            start_date_obj = datetime.strptime(start_date, '%B %Y')
            
            # Handle 'Present' as the end date
            if end_date.lower() == 'present':
                end_date_obj = datetime.now()
            else:
                end_date_obj = datetime.strptime(end_date, '%B %Y')
            
            # Calculate the years of experience
            experience_years = round((end_date_obj - start_date_obj).days / 365.25, 2)

            # Store each experience in a structured format
            experiences.append({
                'role': role,
                'company': company,
                #'location': location,
                'start_date': start_date,
                'end_date': end_date,
                'years_of_experience': experience_years
            })
        return experiences

    def extract_experience_details(self, text):
        company_name_pattern = r"^([SA-Za-z\s,.&]+)\n"  # Adjusted to handle company names properly
        role_pattern = r"(?:\n)?([A-Za-z\s\-]+)\s\|"  # This handles the roles like "Front-end web developer |"
        start_date_pattern = r"\|\s?([A-Za-z]+\s\d{4})\s[–\-—]"  # Adjusted to match the date format
        end_date_pattern = r"[–\-—]\s([A-Za-z]+\s\d{3,4})|Present"  # End date pattern that captures dates including present
        
        
        # Split experiences based on the double newlines separating them
        experiences = text.strip().split("\n\n")
        
        parsed_experiences = []
        
        for exp in experiences:
            lines = exp.splitlines()
            
            # Extract company name
            company_match = re.search(company_name_pattern, exp, re.MULTILINE)
            company_name = company_match.group(1).strip() if company_match else None


            # Extract role
            role_match = re.search(role_pattern, exp, re.MULTILINE)
            role = role_match.group(1).strip() if role_match else None
            
            print("Role: ", role)

            # Extract start date
            start_date_match = re.search(start_date_pattern, exp)
            start_date = start_date_match.group(1).strip() if start_date_match else None
            
            # Extract end date
            end_date_match = re.search(end_date_pattern, exp)
            end_date = end_date_match.group(1).strip() if end_date_match else None
            
            # Parse the start and end dates to calculate years of experience
            if start_date:
                start_date_obj = datetime.strptime(start_date, '%B %Y')
            else:
                start_date_obj = None
            
            if end_date:
                if end_date.lower() == 'present':
                    end_date_obj = datetime.now()
                else:
                    end_date_obj = datetime.strptime(end_date, '%B %Y')
            else:
                end_date_obj = None
            
            # Calculate the years of experience if both dates are available
            if start_date_obj and end_date_obj:
                experience_years = round((end_date_obj - start_date_obj).days / 365.25, 2)
            else:
                experience_years = None
            
            
            # Add the extracted details to the result
            parsed_experiences.append({
                "company_name": company_name,
                "role": role,
                "start_date": start_date,
                "end_date": end_date,
                'years_of_experience': experience_years
            })
        
        return parsed_experiences

if __name__ == "__main__":
    # TODO: Add test code or example usage
    pass
