from typing import Dict, Optional
import pdfplumber
from docx import Document
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentParser:
    """Handles parsing of different document formats (PDF, DOCX)."""
    
    SUPPORTED_FORMATS = {'.pdf', '.docx'}
    
    @staticmethod
    def validate_file(file_path: str) -> bool:
        """Validate if the file exists and is of supported format."""
        path = Path(file_path)
        if not path.exists():
            logger.error(f"File does not exist: {file_path}")
            return False
        if path.suffix.lower() not in DocumentParser.SUPPORTED_FORMATS:
            logger.error(f"Unsupported file format: {path.suffix}")
            return False
        return True
    
    @staticmethod
    def parse_pdf(file_path: str) -> Optional[str]:
        """Extract text from PDF files using pdfplumber."""
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text.strip()
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def parse_docx(file_path: str) -> Optional[str]:
        """Extract text from DOCX files using python-docx."""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            logger.error(f"Error parsing DOCX {file_path}: {str(e)}")
            return None
    
    def parse(self, file_path: str) -> Optional[str]:
        """Main method to parse documents based on their format."""
        if not self.validate_file(file_path):
            return None
            
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self.parse_pdf(file_path)
        elif file_extension == '.docx':
            return self.parse_docx(file_path)
        
        return None

    def parse_multiple(self, file_paths: list) -> Dict[str, str]:
        """Parse multiple documents and return a dictionary of results."""
        results = {}
        for file_path in file_paths:
            content = self.parse(file_path)
            if content:
                results[file_path] = content
        return results
    
if __name__ == "__main__":
    # Initialize parser
    parser = DocumentParser()
    
    # Test PDF parsing
    pdf_path = "data/Resumes/hospitality_resume_sample.pdf"
    print("\nTesting PDF parsing:")
    pdf_content = parser.parse(pdf_path)
    if pdf_content:
        print(f"Successfully parsed PDF: {len(pdf_content)} characters")
    else:
        print("Failed to parse PDF")

    # Test DOCX parsing  
    docx_path = "data/Resumes/web_developer_resume_sample.docx"
    print("\nTesting DOCX parsing:")
    docx_content = parser.parse(docx_path)
    if docx_content:
        print(f"Successfully parsed DOCX: {len(docx_content)} characters")
    else:
        print("Failed to parse DOCX")

    # Test multiple file parsing
    print("\nTesting multiple file parsing:")
    files = [pdf_path, docx_path]
    results = parser.parse_multiple(files)
    print(f"Successfully parsed {len(results)} out of {len(files)} files")