import re

import docx
import PyPDF2


class DocumentParser:
    """Class for parsing resumes and extracting relevant information"""

    def __init__(self):
        # TODO: Initialize any necessary attributes
        pass

    def parse_pdf(self, file_path):
        """

        :param file_path:

        """
        return "Hello World!"

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

    def parse_document(self, file_path):
        """

        :param file_path:

        """
        # Detect file type and call appropriate parsing method
        if file_path.endswith(".pdf"):
            doc = self.parse_pdf(file_path)
        else:
            doc = self.parse_docx(file_path)
        return doc


if __name__ == "__main__":
    # TODO: Add test code or example usage
    pass
