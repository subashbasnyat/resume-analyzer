from resume_analyzer.document_parsing import DocumentParser
from resume_analyzer.preprocessing import TextCleaner

document_parser = DocumentParser()
text_cleaner = TextCleaner()

text = document_parser.parse_document("data/Resumes/web_developer_resume_sample.docx")
print("Text Returned: ", text)
text_cleaner.clean_text(text)
