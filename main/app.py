import sys
import os
import streamlit as st

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.groq_handler import GroqHandler
from lib.text_processor import TextProcessor
from lib.resume_analyzer import ResumeAnalyzer
from utils.config import Config
from utils.logger import setup_logger
from utils.prompt_loader import PromptLoader

# Singleton logger setup (runs only once)
if 'loggers' not in st.session_state:
    Config.validate()  # Validate config once
    st.session_state.loggers = {
        "app": setup_logger("app", f"{Config.LOG_DIR}/app.log"),
        "groq_handler": setup_logger("groq_handler", f"{Config.LOG_DIR}/groq_handler.log"),
        "prompt_loader": setup_logger("prompt_loader", f"{Config.LOG_DIR}/prompt_loader.log"),
        "resume_analyzer": setup_logger("resume_analyzer", f"{Config.LOG_DIR}/resume_analyzer.log"),
        "text_processor": setup_logger("text_processor", f"{Config.LOG_DIR}/text_processor.log")
    }
    st.session_state.loggers["app"].debug("Starting Resume Analyzer application")

loggers = st.session_state.loggers

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
    if st.button("Analyze") and uploaded_file:
        loggers["app"].debug("User clicked Analyze button for file: %s", uploaded_file.name)
        file_extension = uploaded_file.name.split(".")[-1].lower()
        temp_path = f"temp_resume.{file_extension}"
        try:
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            text_processor = TextProcessor(loggers["text_processor"])
            extracted_text = text_processor.extract_text(temp_path, file_extension)
            os.remove(temp_path)
            if extracted_text:
                grok_handler = GroqHandler(loggers["groq_handler"], PromptLoader(Config.PROMPTS_FILE, loggers["prompt_loader"]))
                resume_analyzer = ResumeAnalyzer(grok_handler, loggers["resume_analyzer"], PromptLoader(Config.PROMPTS_FILE, loggers["prompt_loader"]))
                with st.spinner("Analyzing resume... Please wait"):
                    analysis = resume_analyzer.analyze_resume(extracted_text, designation, experience, domain)
                st.markdown("# Resume Analysis")
                st.write(analysis)
            else:
                st.error("Could not extract text.")
                loggers["app"].error("Failed to extract text from %s", uploaded_file.name)
        except Exception as e:
            loggers["app"].error("Error processing resume: %s", str(e))
            st.error(f"Error processing resume: {str(e)}")
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    main()