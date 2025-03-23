# Resume Analyzer

The **Resume Analyzer** is a Streamlit-based web application designed to analyze resumes in PDF or DOCX format. It extracts text from uploaded resumes and uses the Groq API to provide a structured analysis based on user-selected criteria such as designation, experience level, and domain. The app offers features like text extraction, resume scoring, logging, caching, and the ability to download the analysis.

## Technologies Used
- **Python**: Core programming language for the application.
- **Streamlit**: Framework for building the interactive web interface.
- **Groq API**: AI-powered text analysis for resume evaluation.
- **PyMuPDF (fitz)**: Library for extracting text from PDF files.
- **python-docx**: Library for extracting text from DOCX files.
- **python-dotenv**: For managing environment variables (e.g., API keys).
- **Git**: Version control for tracking project changes.
- **Logging**: Custom logging system for debugging and monitoring.

---

## Project Setup Steps

### STEP 1: Project Setup and Initial Git Repository
**GOAL**: Set up the project structure and initialize a Git repository.

#### **Project Setup and Initial Git Repository**
1. **Create the Project Directory and Clone the Empty Repo**
   ```bash
   git clone "URL" 
2. **Navigate to the Project Directory**
    ```bash
   cd resume_analyzer
   ```
3. **Open Project in VS Code**
    ```bash
   code .
   ```

#### **Create the Directory Structure**
- This structure separates app logic (main), reusable libraries (lib), utilities (utils), and data files (data).
- Use the terminal or editor to create:
```bash
resume_analyzer/
├── main/
│   └── app.py
├── lib/
│   ├── groq_handler.py
│   ├── resume_analyzer.py
│   └── text_processor.py
├── utils/
│   ├── config.py
│   ├── logger.py
│   ├── file_utils.py
│   └── prompt_loader.py
├── data/
│   ├── logs/
│   └── prompts.json
├── .env
├── requirements.txt
└── README.md
```

#### **Add a README**
- Create this README.md file with initial content:
``` bash
# Resume Analyzer
A Streamlit app to analyze resumes using the Groq API.
```

#### **Initialize Git**
``` bash 
git add README.md
git status
git commit -m "Initial commit: Project setup with README"
git push origin main
```

### STEP 2: Set Up Dependencies
**GOAL**: Install required packages and configure the environment.

#### **Edit requirements.txt**
``` bash
streamlit
groq
pymupdf
python-docx
python-dotenv
```

#### **Install Dependencies**
``` bash
pip install -r requirements.txt
```

#### **Set Up .env for the Groq API Key**
- Visit Groq Console: https://console.groq.com/keys , sign up/login, and generate an API key.
- Add it to .env:
``` bash
GROQ_API_KEY=your_key_here
``` 

- Add .env to .gitignore to keep secrets safe.

#### **Commit**
```  bash
git add requirements.txt .gitignore
git commit -m "Add dependencies and environment setup"
git push origin main
``` 

### STEP 3: Basic Streamlit App for File Upload
**GOAL**: Create a simple Streamlit app to upload a resume and display its text.

#### **Edit ```main/app.py```**
``` python
import streamlit as st

def main():
    st.title("Resume Analyzer")
    st.subheader("Upload a PDF or Word Resume")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    if uploaded_file:
        st.write("File uploaded:", uploaded_file.name)
        st.write("Text extraction coming soon!")

if __name__ == "__main__":
    main()
``` 

#### **Run the App**
``` bash 
streamlit run main/app.py
```
- You’ll see a title, subtitle, and file uploader. Upload a PDF or DOCX to see the filename.

#### **Commit**
``` bash 
git add main/app.py
git commit -m "Add basic Streamlit app for file upload"
git push origin main
```

### STEP 4: Extract Text from Uploaded Files
**GOAL**: Add text extraction for PDF and DOCX files.

#### **Edit ```lib/text_processor.py```**
``` python
import fitz  # PyMuPDF
from docx import Document

class TextProcessor:
    """A class to process and extract text from PDF and DOCX files."""
    
    def __init__(self):
        pass

    def extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        doc.close()
        return text

    def extract_text_from_docx(self, docx_path):
        doc = Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    def extract_text(self, file_path, file_extension):
        if file_extension == "pdf":
            return self.extract_text_from_pdf(file_path)
        elif file_extension == "docx":
            return self.extract_text_from_docx(file_path)
        return ""
```

#### **Update ```main/app.py```**
``` python
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from lib.text_processor import TextProcessor

def main():
    st.title("Resume Analyzer")
    st.subheader("Upload a PDF or Word Resume")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    if uploaded_file and st.button("Extract Text"):
        file_extension = uploaded_file.name.split(".")[-1].lower()
        temp_path = f"temp_resume.{file_extension}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        processor = TextProcessor()
        extracted_text = processor.extract_text(temp_path, file_extension)
        os.remove(temp_path)
        st.write("Extracted Text:")
        st.text_area("Text", extracted_text, height=300)

if __name__ == "__main__":
    main()
```

#### **Test**
- Run ```streamlit run main/app.py``` , upload a file, and click **```Extract Text```** to see the output.

#### **Commit**
``` bash
git add lib/text_processor.py main/app.py
git commit -m "Add text extraction for PDF and DOCX files"
git push origin main
```

### STEP 5: Set Up Groq API Integration
**GOAL**: Connect to the Groq API to analyze text.

#### **Edit ```utils/config.py```**
``` python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    @staticmethod
    def validate():
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in the .env file")
```

#### **Edit ```lib/groq_handler.py```**
``` python
from groq import Groq
from utils.config import Config

class GroqHandler:
    def __init__(self):
        Config.validate()
        self.client = Groq(api_key=Config.GROQ_API_KEY)

    def analyze_text(self, prompt, text, model="gemma2-9b-it", max_tokens=2000):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt + "\n\n" + text}],
            model=model,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
```

#### **Update ```main/app.py```**
``` python
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from lib.text_processor import TextProcessor
from lib.groq_handler import GroqHandler

def main():
    st.title("Resume Analyzer")
    st.subheader("Upload a PDF or Word Resume")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    if uploaded_file and st.button("Analyze"):
        file_extension = uploaded_file.name.split(".")[-1].lower()
        temp_path = f"temp_resume.{file_extension}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        processor = TextProcessor()
        extracted_text = processor.extract_text(temp_path, file_extension)
        os.remove(temp_path)
        if extracted_text:
            groq = GroqHandler()
            prompt = "Analyze this resume text and summarize its key points."
            with st.spinner("Analyzing..."):
                analysis = groq.analyze_text(prompt, extracted_text)
            st.write("Analysis:")
            st.markdown(analysis)
        else:
            st.error("No text extracted from the file.")

if __name__ == "__main__":
    main()
```

#### **Test**
- Run ```streamlit run main/app.py``` , upload a resume, and click **```Analyze```** to see a summary.

#### **Commit**
``` bash 
git add utils/config.py lib/groq_handler.py main/app.py
git commit -m "Integrate Groq API for basic text analysis"
git push origin main
```

### STEP 6: Add Structured Analysis with Prompts
**GOAL**: Use prompt_loader.py and resume_analyzer.py for structured output.

#### **Update ```utils/config.py```**
``` bash 
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LOG_DIR = "data/logs"
    PROMPTS_FILE = "data/prompts.json"

    @staticmethod
    def validate():
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in the .env file")
```

#### **Edit ```data/prompts.json```**
``` json 
{
  "resume_analysis": {
    "description": "Prompt for analyzing a resume based on designation, experience, and domain",
    "template": "Analyze the following resume text for this context:\n- Desired Designation: {designation}\n- Experience Level: {experience}\n- Domain: {domain}\n\nProvide three sections based ONLY on the explicit resume content:\n1. Strengths: List in bullet points using \"Your\" (Education, Work Experience, Skills, Projects, Certifications, writing style).\n2. Areas to Improve: List in bullet points using \"Your\". If none, say \"- No significant improvements identified.\"\n3. Score: Provide ONE score out of 100 as \"Score: [number]\".\n\nFormat:\nStrengths:\n- Your strength 1\n- Your strength 2\nAreas to Improve:\n- Your area 1\n- Your area 2\nScore: [number]"
  },
  "combine_partial_responses": {
    "description": "Prompt for combining multiple partial responses into a coherent one",
    "template": "Combine multiple partial responses into one coherent response.\nPreserve all details and remove duplicates or conflicts."
  }
}
```

#### **Edit ```utils/prompt_loader.py```**
``` python
import json
import os

class PromptLoader:
    def __init__(self, prompts_file):
        self.prompts_file = prompts_file
        self.prompts = self._load_prompts()

    def _load_prompts(self):
        with open(self.prompts_file, "r", encoding="utf-8") as f:
            prompts = json.load(f)
        return prompts

    def get_prompt(self, prompt_key, **kwargs):
        template = self.prompts[prompt_key]["template"]
        return template.format(**kwargs)
```

#### **Edit ```lib/resume_analyzer.py```**
``` python
class ResumeAnalyzer:
    def __init__(self, groq_handler, prompt_loader):
        self.grok = groq_handler
        self.prompt_loader = prompt_loader

    def analyze_resume(self, text, designation, experience, domain):
        prompt = self.prompt_loader.get_prompt(
            "resume_analysis",
            designation=designation,
            experience=experience,
            domain=domain
        )
        result = self.grok.analyze_text(prompt, text, max_tokens=1500)
        return result
```

#### **Update ```main/app.py```**
``` python 
import sys
import os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.groq_handler import GroqHandler
from lib.text_processor import TextProcessor
from lib.resume_analyzer import ResumeAnalyzer
from utils.config import Config
from utils.prompt_loader import PromptLoader

def main():
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
```

#### **Test**
- Run **```streamlit run main/app.py```** and test with dropdown selections.

#### **Commit**
``` bash 
git add utils/config.py data/prompts.json utils/prompt_loader.py lib/resume_analyzer.py main/app.py
git commit -m "Add structured analysis with prompts and update Config"
git push origin main
```

### STEP 7: Add Logging and Exception Handling
**GOAL**: Enhance with logger.py and error handling.

#### **Edit ```utils/logger.py```**
``` python 
import logging
import os

def setup_logger(name, log_file, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    return logger
```

#### **Update ```lib/text_processor.py```**
``` python
import fitz
from docx import Document

class TextProcessor:
    def __init__(self, logger):
        self.logger = logger

    def extract_text_from_pdf(self, pdf_path):
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
        self.logger.debug("Extracting text from file: %s", file_path)
        if file_extension == "pdf":
            return self.extract_text_from_pdf(file_path)
        elif file_extension == "docx":
            return self.extract_text_from_docx(file_path)
        self.logger.warning("Unsupported file extension: %s", file_extension)
        return ""
```

#### **Update ```main/app.py```**
``` python
import sys
import os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.groq_handler import GroqHandler
from lib.text_processor import TextProcessor
from lib.resume_analyzer import ResumeAnalyzer
from utils.config import Config
from utils.logger import setup_logger
from utils.prompt_loader import PromptLoader

if 'loggers' not in st.session_state:
    Config.validate()
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
                grok_handler = GroqHandler()
                resume_analyzer = ResumeAnalyzer(grok_handler, PromptLoader(Config.PROMPTS_FILE))
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
```

#### **Test**
- Run ```streamlit run main/app.py``` and check logs in ```data/logs/```.

#### **Commit**
``` bash
git add utils/logger.py lib/text_processor.py main/app.py
git commit -m "Add logging and exception handling"
git push origin main
```

### STEP 8: Final Enhancements (Caching, Download, Multi-Page)
**GOAL**: Add caching, download functionality, and multi-page navigation.

#### **Edit ```utils/file_utils.py```**
``` python
import os

def save_text_to_file(text, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
```

#### **Update ```main/app.py```**
``` python
import sys
import os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.groq_handler import GroqHandler
from lib.text_processor import TextProcessor
from lib.resume_analyzer import ResumeAnalyzer
from utils.file_utils import save_text_to_file, remove_file
from utils.logger import setup_logger
from utils.config import Config
from utils.prompt_loader import PromptLoader

if 'loggers' not in st.session_state:
    Config.validate()
    st.session_state.loggers = {
        "app": setup_logger("app", f"{Config.LOG_DIR}/app.log"),
        "groq_handler": setup_logger("groq_handler", f"{Config.LOG_DIR}/groq_handler.log"),
        "prompt_loader": setup_logger("prompt_loader", f"{Config.LOG_DIR}/prompt_loader.log"),
        "resume_analyzer": setup_logger("resume_analyzer", f"{Config.LOG_DIR}/resume_analyzer.log"),
        "text_processor": setup_logger("text_processor", f"{Config.LOG_DIR}/text_processor.log")
    }
    st.session_state.loggers["app"].debug("Starting Resume Analyzer application")

loggers = st.session_state.loggers

@st.cache_resource
def get_grok_handler():
    return GroqHandler()

@st.cache_resource
def get_text_processor():
    return TextProcessor(loggers["text_processor"])

@st.cache_resource
def get_resume_analyzer(_grok_handler):
    return ResumeAnalyzer(_grok_handler, PromptLoader(Config.PROMPTS_FILE))

grok_handler = get_grok_handler()
text_processor = get_text_processor()
resume_analyzer = get_resume_analyzer(grok_handler)

def main():
    if 'page' not in st.session_state:
        st.session_state.page = "upload"
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None
    if 'processed' not in st.session_state:
        st.session_state.processed = False

    if st.session_state.page == "upload":
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
            st.session_state.uploaded_file = uploaded_file
            st.session_state.designation = designation
            st.session_state.experience = experience
            st.session_state.domain = domain
            st.session_state.page = "results"
            st.session_state.processed = False
            st.rerun()

    elif st.session_state.page == "results":
        uploaded_file = st.session_state.uploaded_file
        file_extension = uploaded_file.name.split(".")[-1].lower()
        temp_path = f"temp_resume.{file_extension}"
        try:
            if not st.session_state.processed:
                loggers["app"].debug("Processing uploaded file: %s", uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                extracted_text = text_processor.extract_text(temp_path, file_extension)
                remove_file(temp_path)
                if extracted_text:
                    loggers["app"].debug("Text extracted successfully, length: %d characters", len(extracted_text))
                    with st.spinner("Analyzing resume... Please wait"):
                        st.session_state.analysis = resume_analyzer.analyze_resume(
                            extracted_text, st.session_state.designation, st.session_state.experience, st.session_state.domain
                        )
                        st.session_state.processed = True
                    loggers["app"].debug("Resume analysis completed")
                else:
                    st.error("Could not extract text. Please check the file format.")
                    loggers["app"].error("Failed to extract text from %s", uploaded_file.name)

            if st.session_state.analysis:
                if st.button("Upload New Resume"):
                    loggers["app"].debug("User clicked Upload New Resume")
                    st.session_state.page = "upload"
                    st.session_state.analysis = None
                    st.session_state.processed = False
                    st.rerun()
                st.markdown("# Resume Analysis")
                st.write(st.session_state.analysis)
                output_filename = "resume_analysis.txt"
                save_text_to_file(st.session_state.analysis, output_filename)
                with open(output_filename, "rb") as file:
                    st.download_button(label="Download Analysis", data=file, file_name=output_filename, mime="text/plain")
                remove_file(output_filename)

        except Exception as e:
            loggers["app"].error("Error processing resume: %s", str(e))
            st.error(f"Error processing resume: {str(e)}")
            remove_file(temp_path)

if __name__ == "__main__":
    main()
```

#### **Test**
- Run ```streamlit run main/app.py``` and verify multi-page navigation, caching, and download functionality.

#### **Commit**
``` bash
git add utils/file_utils.py main/app.py
git commit -m "Final enhancements: caching, download, and multi-page navigation"
git push origin main
```

## Running the Application
1. Ensure all dependencies are installed: ```pip install -r requirements.txt```
2. Set up your ```.env``` file with the Groq API key.
3. Run the app: ```streamlit run main/app.py```
4. Open your browser to ```localhost:8501``` to use the app.