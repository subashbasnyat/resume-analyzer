import re
from datetime import datetime


class CandidateExtractor:
    """Class for extracting specific information from resumes or job descriptions."""

    def __init__(self):
        pass

    def extract_name(self, text):
        """Extracts the candidate's name from the given text.

        :param text: str: The text from which the name will be extracted.
        :returns: str: The candidate's name, if found.
        """
        # TODO: Implement name extraction logic
        pass

    def extract_phone_number(self, text):
        """Extracts phone number from the given text using regex.

        :param text: str: The text from which the phone number will be extracted.
        :returns: str: The candidate's phone number, if found.
        """
        phone_pattern = r'\+?\d{1,4}?[\s.-]?\(?\d{1,4}?\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,9}'
        phone_match = re.search(phone_pattern, text)
        return phone_match.group() if phone_match else None

    def extract_skills(self, text):
        """Extracts skills from the given text using a predefined list of skills or keyword matching.

        :param text: str: The text from which the skills will be extracted.
        :returns: list: A list of extracted skills.
        """
        # TODO: Use NLP, predefined skill list, or keyword extraction techniques
        pass

    def extract_employment_details(self, text):
        """Extracts employment details (job titles, company names, employment duration) from the given text.

        :param text: str: The text from which employment details will be extracted.
        :returns: list: A list of dictionaries containing job details.
        """
        # Focus on the "Experience" section only
        experience_section = re.search(r"Experience\s(.+?)(Education|$)", text, re.DOTALL)
        if experience_section:
            text = experience_section.group(1).strip()
        
        experience_pattern = r"^(.*?)\s+([A-Za-z\s\-]+)\s*\|\s*([A-Za-z]+\s\d{4})\s*[–\-—]\s*([A-Za-z]+\s\d{4}|Present)"
        matches = re.findall(experience_pattern, text, re.MULTILINE)
        
        parsed_experiences = []
        
        for match in matches:
            company_name = match[0].strip()
            role = match[1].strip()
            start_date = match[2].strip()
            end_date = match[3].strip()
            
            try:
                start_date_obj = datetime.strptime(start_date, '%B %Y')
                end_date_obj = datetime.now() if end_date.lower() == 'present' else datetime.strptime(end_date, '%B %Y')
                experience_years = round((end_date_obj - start_date_obj).days / 365.25, 2)
            except ValueError:
                experience_years = None

            parsed_experiences.append({
                "company_name": company_name,
                "role": role,
                "start_date": start_date,
                "end_date": end_date,
                'years_of_experience': experience_years
            })
        
        return parsed_experiences

    def extract_urls(self, text):
        """Extracts URLs (like LinkedIn) from the given text using regex.

        :param text: str: The text from which the URLs will be extracted.
        :returns: list: A list of URLs found in the text.
        """
        linkedin_pattern = r'linkedin\.com\/[a-zA-Z0-9\-_\/]+'
        linkedin_urls = re.findall(linkedin_pattern, text)
        
        # Also keep the general URL pattern for other URLs
        general_url_pattern = r'https?://[^\s]+'
        other_urls = [url for url in re.findall(general_url_pattern, text) 
                     if 'linkedin.com' not in url]
        
        return {
            'linkedin': linkedin_urls[0] if linkedin_urls else None,
            'other_urls': other_urls
        }

    def extract_email(self, text):
        """Extracts email addresses from the given text using regex.

        :param text: str: The text from which the email addresses will be extracted.
        :returns: str: The candidate's email address, if found.
        """
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, text)
        return email_match.group() if email_match else None

    def extract_years_of_experience(self, text):
        """Extracts years of experience from the given text using regex.

        :param text: str: The text from which years of experience will be extracted.
        :returns: list: List of extracted years of experience mentions.
        """
        experience_pattern = r'(\d+)\s*(?:year|years|yrs)\s*(?:of)?\s*(?:experience)?'
        experience_matches = re.findall(experience_pattern, text.lower())
        return [int(years) for years in experience_matches] if experience_matches else None

    def extract_contact_info(self, text):
        """Extracts all contact-related information from the given text.

        :param text: str: The text from which contact information will be extracted.
        :returns: dict: A dictionary containing all contact information.
        """
        return {
            'email': self.extract_email(text),
            'phone': self.extract_phone_number(text),
            'urls': self.extract_urls(text),
            'years_of_experience': self.extract_years_of_experience(text)
        }

    def extract_all(self, text):
        """Extracts all relevant information from the given text.

        :param text: str: The text from which all information will be extracted.
        :returns: dict: A dictionary with all extracted information.
        """
        contact_info = self.extract_contact_info(text)
        return {
            'name': self.extract_name(text),
            'contact_info': contact_info,
            'employment_details': self.extract_employment_details(text),
            'skills': self.extract_skills(text)
        }

