import pandas as pd
from pathlib import Path
from typing import List, Any
from nltk.downloader import Downloader
import logging
from spacy.cli import download
from resume_analyzer.document_parsing import DocumentParser
from resume_analyzer.preprocessing import TextCleaner
from resume_analyzer.vectorization import TextVectorizer
from resume_analyzer.extraction import CandidateExtractor

download("en_core_web_sm")


def check_package_exists(
    package_id: Any,
    download_dir: Path,
) -> bool:
    downloader = Downloader(download_dir=str(download_dir))
    return downloader.is_installed(package_id)


def download_nltk_data(
    list_of_resources: List[str],
    download_dir: Path,
) -> None:
    download_dir.mkdir(parents=True, exist_ok=True)
    downloader = Downloader(download_dir=str(download_dir))
    for resource in list_of_resources:
        if not check_package_exists(resource, download_dir):
            logging.debug(f'Downloading {resource} to {download_dir}')
            downloader.download(info_or_id=resource, quiet=True)
        else:
            logging.debug(f'{resource} already exists in {download_dir}')


download_nltk_data(
    list_of_resources=[
        'stopwords',
        'punkt',
    ],
    download_dir=Path('./data/nltk/'),
)


skills_df = pd.read_csv("data/skills_list.csv")
skills_list = skills_df['skill_name'].dropna().tolist()

document_parser = DocumentParser(skills_list)
text_cleaner = TextCleaner()
extractor = CandidateExtractor()
vectorizer = TextVectorizer()


resume = document_parser.parse_document(
    "data/Resumes/web_developer_resume_sample.docx")
cleaned_resume = ' '.join(text_cleaner.clean_text(resume))

jd = document_parser.parse_document(
    "data/JDs/web_developer_job_description_sample.docx")
cleaned_jd = ' '.join(text_cleaner.clean_text(jd))
print("Cleaned Resume: ", cleaned_resume)
print("Cleaned JD: ", cleaned_jd)


extractions = extractor.extract_all(cleaned_resume)
print("Extractions: ", extractions)

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
