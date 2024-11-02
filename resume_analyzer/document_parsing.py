import re

import docx
import PyPDF2
import pandas as pd
from flashtext import KeywordProcessor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentParser:
    """Class for parsing resumes and extracting relevant information"""

    def __init__(self, skills_list):
        """
        Initializes the DocumentParser with a list of skills.

        :param skills_list: List of skills to be used for similarity calculation.
        """
        self.skills_list = skills_list

    def parse_pdf(self, file_path):
        """

        :param file_path:

        """
        # TODO: Implement PDF parsing
        pass

    def parse_docx(self, file_path):
        """Extracts, concatenates, and cleans text from paragraphs and tables in a DOCX file,
        removing excessive spaces and empty lines.

        :param file_path: Document
        :returns: str: The cleaned text from all paragraphs and tables in the DOCX file.

        """
        fullText = []
        doc_file = docx.Document(file_path)

        # Extract text from paragraphs
        fullText.extend([para.text for para in doc_file.paragraphs])

        # Extract text from tables
        for table in doc_file.tables:
            for row in table.rows:
                for cell in row.cells:
                    fullText.append(cell.text)

        # Join all extracted text and clean up whitespace using regex
        # Join paragraphs and table text with newlines
        text = "\n".join(fullText)
        # Replace multiple spaces/newlines with a single space
        cleaned_text = re.sub(r"\s+", " ", text)
        # Strip any leading/trailing spaces
        return cleaned_text.strip()
    
    def extract_skills(self, resume_text):
        """
        Extracts skills from the resume text based on the provided skills list.

        :param resume_text: Text content of the resume.
        :returns: list: List of unique skills found in the resume.
        """
        keyword_processor = KeywordProcessor(case_sensitive=False)
        keyword_processor.add_keywords_from_list(self.skills_list)
        extracted_skills = keyword_processor.extract_keywords(resume_text)
        return list(set(extracted_skills))
    
    def calculate_cosine_similarity(self, resume_text):
        """
        Calculates cosine similarity between resume text and skills list.

        :param resume_text: Text content of the resume.
        :returns: DataFrame: Skills with their cosine similarity scores.
        """
        # Extract relevant skills from resume text
        extracted_skills = self.extract_skills(resume_text)

        # Combine resume text and skills for TF-IDF vectorization
        documents = [resume_text] + extracted_skills

        # Calculate TF-IDF vectors
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

        # Calculate cosine similarity between resume and each skill
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        # Create a DataFrame to display skills with their similarity scores
        similarity_scores = pd.DataFrame({'Skill': extracted_skills, 'Cosine Similarity': cosine_similarities})
        return similarity_scores.sort_values(by='Cosine Similarity', ascending=False)

    def parse_document(self, file_path):
        """
        Detects the file type and parses the document accordingly.

        :param file_path: Path to the document (PDF or DOCX).
        :returns: str: The parsed text from the document.
        """
        if file_path.endswith('.pdf'):
            return self.parse_pdf(file_path)
        elif file_path.endswith('.docx'):
            return self.parse_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Please use a PDF or DOCX file.")
        
    def analyze_resume(self, file_path):
        """
        Parses a resume file and calculates cosine similarity for relevant skills.

        :param file_path: Path to the resume file.
        :returns: DataFrame: Skills with their cosine similarity scores.
        """
        # Parse document and retrieve resume text
        resume_text = self.parse_document(file_path)
        
        # Calculate cosine similarity scores for the extracted skills
        return self.calculate_cosine_similarity(resume_text)


if __name__ == "__main__":
    # Load skills list from CSV file
    skills_df = pd.read_csv("data/skills_list.csv")
    skills_list = skills_df['skill_name'].dropna().tolist()

    # Create a DocumentParser instance with the skills list
    parser = DocumentParser(skills_list)

    # Analyze resume for cosine similarity on relevant skills
    similarity_scores = parser.analyze_resume("data/Resumes/web_developer_resume_sample.docx")