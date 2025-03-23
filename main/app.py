import sys
import os
import streamlit as st

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.groq_handler import GroqHandler
from lib.text_processor import TextProcessor
from lib.resume_analyzer import ResumeAnalyzer
from utils.config import Config
from utils.prompt_loader import PromptLoader

def main():
    """Main function to run the Streamlit Resume Analyzer app."""
    st.title("Resume Analyzer")
    st.subheader("Upload a PDF or Word Resume")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    col1, col2, col3 = st.columns(3)
    with col1:
        designation = st.selectbox("Select Desired Designation", ["Data Scientist", "Data Analyst", "MLOps Engineer", "Machine Learning Engineer"])
    with col2:
        experience = st.selectbox("Select Experience Level", ["Fresher", "<1 Year Experience", "1-2 Years Experience", "2-5 Years Experience", "5-8 Years Experience", "8-10 Years Experience"])
    with col3:
        domain = st.selectbox("Select Domain", ["Finance", "Healthcare", "Automobile", "Real Estate"])
    if uploaded_file and st.button("Analyze"):
        file_extension = uploaded_file.name.split(".")[-1].lower()
        temp_path = f"temp_resume.{file_extension}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        text_processor = TextProcessor()
        extracted_text = text_processor.extract_text(temp_path, file_extension)
        os.remove(temp_path)
        if extracted_text:
            grok_handler = GroqHandler()
            prompt_loader = PromptLoader(Config.PROMPTS_FILE)
            resume_analyzer = ResumeAnalyzer(grok_handler, prompt_loader)
            with st.spinner("Analyzing resume... Please wait"):
                analysis = resume_analyzer.analyze_resume(extracted_text, designation, experience, domain)
            st.markdown("# Resume Analysis")
            st.write(analysis)
        else:
            st.error("Could not extract text.")

if __name__ == "__main__":
    main()