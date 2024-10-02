# Resume Analyzer

This project aims to develop a resume evaluation model to improve the hiring process by
extracting and matching resume data to job descriptions.

# Usage

1. Install the requirements

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. Download punkt-tab

```bash
nltk.download('punkt_tab')
```

3. Download stopwords

```bash
nltk.download('stopwords')
```

4. Run the processing script

```bash
python process.py
```
