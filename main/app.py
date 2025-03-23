import os  # Operating system interfaces for file handling
import sys
# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st  # Web app framework for creating interactive interfaces
from lib.text_processor import TextProcessor  # Custom class for text extraction

def main():
    """Main function to run the Streamlit Resume Analyzer application."""
    # Set the title of the web application
    st.title("Resume Analyzer")
    # Add a subheader to provide context
    st.subheader("Upload a PDF or Word Resume")
    
    # Create a file uploader widget accepting PDF and DOCX files
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Check if a file is uploaded and extract button is clicked
    if uploaded_file and st.button("Extract Text"):
        # Get the file extension from the uploaded file name
        file_extension = uploaded_file.name.split(".")[-1].lower()
        # Define a temporary file path for processing
        temp_path = f"temp_resume.{file_extension}"
        
        # Save the uploaded file temporarily to disk
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Create an instance of TextProcessor to handle text extraction
        processor = TextProcessor()
        # Extract text using the appropriate method based on file extension
        extracted_text = processor.extract_text(temp_path, file_extension)
        
        # Clean up by removing the temporary file
        os.remove(temp_path)
        
        # Display the extracted text section
        st.write("Extracted Text:")
        # Show the extracted text in a scrollable text area
        st.text_area("Text", extracted_text, height=300)
# Entry point of the script - runs the application when executed directly.
if __name__ == "__main__":
    main()