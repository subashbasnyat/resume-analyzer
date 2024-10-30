import re
import unicodedata

from bs4 import BeautifulSoup
import spacy
from spacy.lang.en import English
import contractions
from datetime import datetime

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
        return BeautifulSoup(text, 'html.parser').get_text()

    def remove_accented_chars_func(self, text):
        """Removes all accented characters from a string, if present.

        :param text: str: The string from which accented characters will be removed.
        :returns: str: The cleaned string without accented characters.

        """
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation_func(self, text):
        """Removes all punctuation from a string.

        :param text: str: The string from which punctuation will be removed.
        :returns: str: The cleaned string without punctuation.

        """
        return re.sub(r'[^a-zA-Z0-9]', ' ', text)

    def remove_extra_whitespaces_func(self, text):
        """Removes extra whitespaces from a string, if present.

        :param text: str: The string from which extra whitespaces will be removed.
        :returns: str: The cleaned string without extra whitespaces.

        """
        return re.sub(r'^\s*|\s\s*', ' ', text).strip()

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

    def clean_text(self, text):
        """Applies all cleaning steps to the given text.

        :param text: str: The string to be cleaned.
        :returns: list: A list of cleaned and tokenized words.

        """
        lowercased = self.lowercase_text(text)
        expanded = self.expand_contractions(lowercased)
        no_html = self.remove_html_tags_func(expanded)
        no_accented_chars = self.remove_accented_chars_func(no_html)
        no_punct = self.remove_punctuation_func(no_accented_chars)
        no_extra_whitespaces = self.remove_extra_whitespaces_func(no_punct)
        no_stopwords = self.remove_stopwords(no_extra_whitespaces)
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
        
        # Focus on the "Experience" section only
        experience_section = re.search(r"Experience\s(.+?)(Education|$)", text, re.DOTALL)
        if experience_section:
            text = experience_section.group(1).strip()
        """
        company_name_pattern = r"^([A-Za-z\s,.&-]+)"  # Adjusted to handle company names properly
        role_pattern = r"(?:\n)?([A-Za-z\s\-]+)\s\|"  # This handles the roles like "Front-end web developer |"
        start_date_pattern = r"\|\s?([A-Za-z]+\s\d{4})\s[–\-—]"  # Adjusted to match the date format
        end_date_pattern = r"[–\-—]\s([A-Za-z]+\s\d{4})|Present"  # End date pattern that captures dates including present
        
        
        # Split experiences based on the double newlines separating them
        experiences = text.strip().split("\n\n")
        
        parsed_experiences = []
        
        for exp in experiences:
            
            # Process each line separately within an experience block
            lines = exp.splitlines()
            
            # Extract company name
            company_match = re.search(company_name_pattern, exp, re.MULTILINE)
            company_name = company_match.group(1).strip() if company_match else None


            # Extract role
            role_match = re.search(role_pattern, exp, re.MULTILINE)
            role = role_match.group(1).strip() if role_match else None

            # Extract start date
            # start_date_match = re.search(start_date_pattern, exp)
            start_date_match = re.search(start_date_pattern, exp)
            start_date = start_date_match.group(1).strip() if start_date_match else None
            
            # Extract end date
            # end_date_match = re.search(end_date_pattern, exp)
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
    """
        # Adjusted patterns for extracting details
        experience_pattern = r"^(.*?)\s+([A-Za-z\s\-]+)\s*\|\s*([A-Za-z]+\s\d{4})\s*[–\-—]\s*([A-Za-z]+\s\d{4}|Present)"  # Matches company, role, start, and end date
        
        # Split experiences based on double newlines separating them
        matches = re.findall(experience_pattern, text)
        
        parsed_experiences = []
        
        for match in matches:
            # Find all matches for the experience pattern in the current experience block
                           
            company_name = match[0].strip()
            role = match[1].strip()
            start_date = match[2].strip()
            end_date = match[3].strip()
            
            # Parse the start and end dates to calculate years of experience
            try:
                start_date_obj = datetime.strptime(start_date, '%B %Y')
                end_date_obj = datetime.now() if end_date.lower() == 'present' else datetime.strptime(end_date, '%B %Y')
                
                # Calculate years of experience
                experience_years = round((end_date_obj - start_date_obj).days / 365.25, 2)
            except ValueError:
                # If dates don't parse, set years_of_experience to None
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
