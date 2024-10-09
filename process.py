from resume_analyzer.document_parsing import DocumentParser
from resume_analyzer.preprocessing import TextCleaner

document_parser = DocumentParser()
text_cleaner = TextCleaner()


resume = document_parser.parse_document(
    "data/Resumes/web_developer_resume_sample.docx")
cleaned_resume = text_cleaner.clean_text(resume)
jd = document_parser.parse_document(
    "data/JDs/web_developer_job_description_sample.docx")
cleaned_jd = text_cleaner.clean_text(jd)
print("Cleaned Resume: ", cleaned_resume)
print("Cleaned JD: ", cleaned_jd)
