import fitz  # PyMuPDF
from docx import Document

class TextProcessor:
    """Class to extract text from PDF and DOCX files."""
    def __init__(self, logger):
        self.logger = logger

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file."""
        self.logger.debug("Extracting text from PDF: %s", pdf_path)
        try:
            doc = fitz.open(pdf_path)
            text = "\n".join([page.get_text("text") for page in doc])
            doc.close()
            self.logger.debug("Text extracted from PDF: %s", pdf_path)
            return text
        except Exception as e:
            self.logger.error("Error extracting text from PDF %s: %s", pdf_path, str(e))
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def extract_text_from_docx(self, docx_path):
        """Extract text from a DOCX file."""
        self.logger.debug("Extracting text from DOCX: %s", docx_path)
        try:
            doc = Document(docx_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            self.logger.debug("Text extracted from DOCX: %s", docx_path)
            return text
        except Exception as e:
            self.logger.error("Error extracting text from DOCX %s: %s", docx_path, str(e))
            raise Exception(f"Error extracting text from DOCX: {str(e)}")

    def extract_text(self, file_path, file_extension):
        """Extract text based on file extension."""
        self.logger.debug("Extracting text from file: %s", file_path)
        if file_extension == "pdf":
            return self.extract_text_from_pdf(file_path)
        elif file_extension == "docx":
            return self.extract_text_from_docx(file_path)
        self.logger.warning("Unsupported file extension: %s", file_extension)
        return ""