import re
import logging
from typing import Dict, List, Any

import spacy
from spacy import displacy


class InformationExtractor:
    def __init__(self):
        try:
            # Load spaCy model for NLP tasks
            self.nlp = spacy.load("en_core_web_sm")
            self.combined_patterns_path = "data/combined_patterns.jsonl"
            self.ruler = self.nlp.add_pipe("entity_ruler")
            self.ruler.from_disk(self.combined_patterns_path)

        except Exception as e:
            logging.error(f"Error loading spaCy model: {str(e)}")
            raise

        # Regex patterns
        self.email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        self.phone_pattern = r"\b(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b"
        self.experience_pattern = r"(\d+)\s*\+?\s*(?:year|yr)s?\s*of\s*experience"

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information from text."""
        if not text:
            return {"email": None, "phone": None, "location": None}

        # Email extraction
        email_match = re.search(self.email_pattern, text)
        email = email_match.group() if email_match else None

        # Phone extraction
        phone_match = re.search(self.phone_pattern, text)
        phone = phone_match.group() if phone_match else None

        # Location extraction
        doc = self.nlp(text)
        locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
        location = locations[0] if locations else None

        return {"email": email, "phone": phone, "location": location}

    def extract_education(self, text: str) -> List[Dict[str, Any]]:

        text = text.lower()
        doc = self.nlp(text)
        myset = []
        subset = []
        for ent in doc.ents:
            if ent.label_ == "DEGREE":
                subset.append(ent.text)
        myset.append(subset)
        return list(set(subset))

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using predefined skills list."""
        doc = self.nlp(text)
        myset = []
        subset = []
        for ent in doc.ents:
            if ent.label_ == "SKILL":
                subset.append(ent.text)
        myset.append(subset)
        return list(set(subset))

    def extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract years of experience from text."""
        experience_matches = re.findall(self.experience_pattern, text, re.IGNORECASE)

        return (
            [{"years": int(years)} for years in experience_matches]
            if experience_matches
            else []
        )

    def extract_job_titles(self, text: str) -> List[str]:
        doc = self.nlp(text)
        myset = []
        subset = []
        for ent in doc.ents:
            if ent.label_ == "JOB":
                subset.append(ent.text)
        myset.append(subset)
        return list(set(subset))


def extract_resume_and_job_description(
    resume_text: str, job_description_text: str
) -> Dict[str, Any]:
    """Comprehensive extraction of resume and job description."""
    if not resume_text or not job_description_text:
        return {"resume": {}, "job_description": {}}

    extractor = InformationExtractor()

    options = {
        "ents": [
            "SKILL",
            "JOB",
            "DEGREE",
            "GPE",
            "DATE",
            "ORDINAL",
        ]
    }

    return {
        "resume": {
            "job_titles": extractor.extract_job_titles(resume_text),
            "contact": extractor.extract_contact_info(resume_text),
            "education": extractor.extract_education(resume_text),
            "experience": extractor.extract_experience(resume_text),
            "skills": extractor.extract_skills(resume_text),
            "ner": [
                displacy.render(
                    extractor.nlp(resume_text), style="ent", options=options, page=True
                ).replace("\n", "")
            ],
        },
        "job_description": {
            "job_titles": extractor.extract_job_titles(job_description_text),
            "education": extractor.extract_education(job_description_text),
            "experience": extractor.extract_experience(job_description_text),
            "skills": extractor.extract_skills(job_description_text),
            "ner": [
                displacy.render(
                    extractor.nlp(job_description_text),
                    style="ent",
                    options=options,
                    page=True,
                ).replace("\n", "")
            ],
        },
    }


# Example usage
if __name__ == "__main__":
    # Sample texts
    resume_text = """
        John Doe
        Email: john.doe@email.com
        Phone: 5551234567
        New York, NY

        EDUCATION
        University of Washington
        Bachelor of Science in Computer Science
        Graduation: May 2019

        Coursework: Algorithms and Data Structures, Software Engineering, Machine Learning, Cloud Computing
        Achievements: Dean's List (4 semesters), Computer Science Club President
        
        EXPERIENCE
        Senior Software Engineer
        Tesla, Palo Alto, CA
        June 2019 - Present
        • Architectural Leadership: Led the design and implementation of a microservices-based architecture, improving scalability and reducing system downtime by 35%.
        • CI/CD Automation: Spearheaded the creation of a CI/CD pipeline using Jenkins, integrating automated testing, code quality analysis, and deployment, which decreased time-to-production by 50%.
        • Mentorship and Training: Mentored 10+ junior engineers, providing guidance on software best practices, code reviews, and technical skill development.
        • Collaborative Innovation: Partnered with cross-functional teams, including QA, product management, and UI/UX, to deliver high-impact software solutions for Tesla's autonomous driving systems.
        • Containerization and Orchestration: Developed and deployed containerized applications using Docker and Kubernetes, streamlining deployment processes and improving development environment parity.
        • Performance Optimization: Identified and resolved bottlenecks in legacy systems, achieving a 20% improvement in system performance.
        
        Software Engineering Intern
        Google, New York, NY
        May 2018
        • Contributed to the development of a large-scale distributed system, implementing key components that improved data processing efficiency by 25%.
        • Wrote unit tests and performed code reviews to ensure code quality and maintainability.
        • Collaborated with a global team to prototype a new feature for Google Drive, enhancing file-sharing capabilities.
        
        SKILLS
        • Programming Languages: Python, Java, JavaScript, C++
        • Cloud Platforms: AWS (EC2, S3, Lambda), Google Cloud Platform (GCP)
        • DevOps Tools: Docker, Kubernetes, Jenkins, GitLab CI/CD
        • Frameworks: Spring Boot, Flask, React.js
        • Databases: PostgreSQL, MongoDB, DynamoDB
        • Other: RESTful API development, GraphQL, Agile/Scrum methodologies

        PROJECTS
        Smart Fleet Management System
        • Designed a scalable, cloud-based fleet management system to monitor and optimize vehicle routes and energy consumption for electric vehicles.
        • Integrated machine learning models for predictive maintenance, reducing downtime by 15%.
        
        Personal Finance App
        • Developed a personal finance management app using React.js and Flask, featuring budget tracking, expense categorization, and data visualization.
        • Deployed on AWS with Docker containers, supporting 500+ daily active users.
    """
    job_description_text = """
        Title: Senior Data Scientist
        Responsibilities:
        - Design and implement scalable machine learning models.
        - Collaborate with engineering teams to integrate models into production systems.
        - Lead data analysis initiatives to provide actionable business insights.
        - Mentor junior data scientists and analysts.
        Requirements:
        - Master's degree or PhD in Computer Science, Statistics, or related field.
        - 5+ years of experience in data science or machine learning.
        - Strong proficiency in Python, R, and SQL.
        - Experience with cloud platforms like AWS or Azure.
        - Excellent communication and presentation skills.
    """

    extracted_data = extract_resume_and_job_description(
        resume_text, job_description_text
    )

    print(extracted_data)
