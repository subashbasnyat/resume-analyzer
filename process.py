from resume_analyzer.document_parsing import DocumentParser
from resume_analyzer.extraction import InformationExtractor, extract_resume_and_job_description
from resume_analyzer.preprocessing import TextCleaner
from resume_analyzer.vectorization import TextVectorizer
from resume_analyzer.scoring import ResumeScorer

class ResumeProcessor:
    def __init__(self):
        self.parser = DocumentParser()
        self.extractor = InformationExtractor()
        self.cleaner = TextCleaner()
        self.scorer = ResumeScorer()

    def process_resume(self, resume_path, jd_path):
        # Step 1: Parse the resume and job description
        resume_text = self.parser.parse(resume_path)
        jd_text = self.parser.parse(jd_path)
        
        extracted_data = extract_resume_and_job_description(
            resume_text, 
            jd_text, 
        )

        extracted_data['resume']['full_text'] = self.cleaner.clean_text(resume_text)
        extracted_data['job_description']['full_text'] = self.cleaner.clean_text(jd_text)

        # Step 4: Score the resume against the job description
        scores = self.scorer.score_resume(extracted_data)
        
        return scores

if __name__ == "__main__":
    processor = ResumeProcessor()
    
    resume_path = "data/Resumes/web_developer_resume_sample.pdf"
    jd_path = "data/JDs/web_developer_job_description_sample.docx"
    
    result = processor.process_resume(resume_path, jd_path)
