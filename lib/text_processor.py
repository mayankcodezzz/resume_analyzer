import fitz  # type: ignore # PyMuPDF - Library for handling PDF files
from docx import Document  # Library for handling Word (.docx) files

class TextProcessor:
    """A class to process and extract text from PDF and DOCX files."""
    
    def __init__(self):
        """Initialize the TextProcessor class.
        Currently no initialization parameters are needed."""
        pass

    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file to be processed
            
        Returns:
            str: Extracted text from all pages joined by newlines
        """
        # Open the PDF file using PyMuPDF
        doc = fitz.open(pdf_path)
        # Extract text from each page and join with newline characters
        text = "\n".join([page.get_text("text") for page in doc])
        # Close the document to free up resources
        doc.close()
        return text

    def extract_text_from_docx(self, docx_path):
        """Extract text content from a DOCX file.
        
        Args:
            docx_path (str): Path to the DOCX file to be processed
            
        Returns:
            str: Extracted text from all paragraphs joined by newlines
        """
        # Open the DOCX file using python-docx
        doc = Document(docx_path)
        # Extract text from each paragraph and join with newline characters
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    def extract_text(self, file_path, file_extension):
        """Extract text from a file based on its extension.
        
        Args:
            file_path (str): Path to the file to be processed
            file_extension (str): File extension (without dot) to determine processing method
            
        Returns:
            str: Extracted text from the file, empty string if extension not supported
        """
        # Handle PDF files
        if file_extension == "pdf":
            return self.extract_text_from_pdf(file_path)
        # Handle DOCX files
        elif file_extension == "docx":
            return self.extract_text_from_docx(file_path)
        # Return empty string for unsupported file types
        return ""