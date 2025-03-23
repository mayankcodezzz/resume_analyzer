import os  # Operating system interfaces for file handling
import sys
# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st  # Web app framework for creating interactive interfaces
from lib.text_processor import TextProcessor  # Custom class for text extraction
from lib.groq_handler import GroqHandler  # Custom class for interacting with Groq API

def main():
    """Main function to run the Streamlit Resume Analyzer application."""
    # Set the title of the web application
    st.title("Resume Analyzer")
    # Add a subheader to provide context for the user
    st.subheader("Upload a PDF or Word Resume")
    
    # Create a file uploader widget accepting PDF and DOCX files
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Check if a file is uploaded and the Analyze button is clicked
    if uploaded_file and st.button("Analyze"):
        # Extract the file extension from the uploaded file name
        file_extension = uploaded_file.name.split(".")[-1].lower()
        # Define a temporary file path for processing
        temp_path = f"temp_resume.{file_extension}"
        
        # Save the uploaded file temporarily to disk in binary write mode
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Instantiate TextProcessor to extract text from the file
        processor = TextProcessor()
        # Extract text based on the file type
        extracted_text = processor.extract_text(temp_path, file_extension)
        
        # Remove the temporary file to clean up
        os.remove(temp_path)
        
        # Proceed if text was successfully extracted
        if extracted_text:
            # Instantiate GroqHandler for text analysis
            groq = GroqHandler()
            # Define the prompt for Groq API analysis
            prompt = "Analyze this resume text and summarize its key points."
            
            # Display a spinner while analysis is in progress
            with st.spinner("Analyzing..."):
                # Analyze the extracted text using Groq API
                analysis = groq.analyze_text(prompt, extracted_text)
            
            # Display the analysis header
            st.write("Analysis:")
            # Render the analysis result as markdown for better formatting
            st.markdown(analysis)
        else:
            # Display an error message if no text was extracted
            st.error("No text extracted from the file.")

# Entry point of the script - runs the application when executed directly.
if __name__ == "__main__":
    main()