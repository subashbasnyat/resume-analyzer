from resume_analyzer.document_parsing import DocumentParser
from resume_analyzer.preprocessing import TextCleaner
from resume_analyzer.vectorization import TextVectorizer

document_parser = DocumentParser()
text_cleaner = TextCleaner()
vectorizer = TextVectorizer()


resume = document_parser.parse_document(
    "data/Resumes/web_developer_resume_sample.docx")
cleaned_resume = ' '.join(text_cleaner.clean_text(resume))

jd = document_parser.parse_document(
    "data/JDs/web_developer_job_description_sample.docx")
cleaned_jd = ' '.join(text_cleaner.clean_text(jd))
print("Cleaned Resume: ", cleaned_resume)
print("Cleaned JD: ", cleaned_jd)

# Train the Doc2Vec model on both resume and JD
vectorizer.train_model([cleaned_resume, cleaned_jd])

# Vectorize the resume and JD
resume_vector = vectorizer.vectorize(cleaned_resume)
jd_vector = vectorizer.vectorize(cleaned_jd)

print("Resume Vector: ", resume_vector)
print("JD Vector: ", jd_vector)

# Compute the similarity between resume and JD
similarity = vectorizer.compute_similarity(resume_vector, jd_vector)

print(f"Similarity between Resume and JD: {similarity:.4f}")