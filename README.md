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
# Import the Streamlit library for creating web applications
import streamlit as st

# Define the main function that runs the application
def main():
    # Display a title on the web page
    st.title("Resume Analyzer")
    
    # Display a subheader below the title
    st.subheader("Upload a PDF or Word Resume")
    
    # Create a file uploader widget that accepts PDF and Word documents
    # Returns the uploaded file object or None if no file is uploaded
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Check if a file has been uploaded
    if uploaded_file:
        # Display the name of the uploaded file
        st.write("File uploaded:", uploaded_file.name)
        
        # Display a placeholder message indicating future functionality
        st.write("Text extraction coming soon!")

# Standard Python idiom to run the main function when script is executed
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
# Import PyMuPDF library for PDF processing
import fitz  # PyMuPDF

# Import Document class from python-docx library for Word document processing
from docx import Document

class TextProcessor:
    """A class to process and extract text from PDF and DOCX files."""
    
    def __init__(self):
        """Initialize the TextProcessor class."""
        # Empty constructor as no initialization is needed
        pass

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text from all pages
        """
        # Open the PDF file
        doc = fitz.open(pdf_path)
        # Extract text from each page and join with newlines
        text = "\n".join([page.get_text("text") for page in doc])
        # Close the document to free resources
        doc.close()
        # Return the extracted text
        return text

    def extract_text_from_docx(self, docx_path):
        """Extract text from a DOCX file.
        
        Args:
            docx_path (str): Path to the DOCX file
            
        Returns:
            str: Extracted text from all paragraphs
        """
        # Open the Word document
        doc = Document(docx_path)
        # Extract text from each paragraph and join with newlines
        text = "\n".join([para.text for para in doc.paragraphs])
        # Return the extracted text
        return text

    def extract_text(self, file_path, file_extension):
        """Extract text based on file extension.
        
        Args:
            file_path (str): Path to the file
            file_extension (str): File extension ('pdf' or 'docx')
            
        Returns:
            str: Extracted text or empty string if extension not supported
        """
        # Check file extension and call appropriate extraction method
        if file_extension == "pdf":
            return self.extract_text_from_pdf(file_path)
        elif file_extension == "docx":
            return self.extract_text_from_docx(file_path)
        # Return empty string for unsupported file types
        return ""
```

#### **Update ```main/app.py```**
``` python
# Import os module for operating system interactions
import os
# Import sys module for system-specific parameters and functions
import sys
# Add parent directory to system path to allow importing from lib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import Streamlit library for web application
import streamlit as st
# Import TextProcessor class from custom lib module
from lib.text_processor import TextProcessor

def main():
    """Main function to run the Resume Analyzer web application."""
    # Display main title on the page
    st.title("Resume Analyzer")
    
    # Display subheader for file upload section
    st.subheader("Upload a PDF or Word Resume")
    
    # Create file uploader widget accepting PDF and DOCX files
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Check if file is uploaded and extract button is clicked
    if uploaded_file and st.button("Extract Text"):
        # Get file extension from uploaded filename
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        # Define temporary file path for processing
        temp_path = f"temp_resume.{file_extension}"
        
        # Save uploaded file to temporary location
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Create instance of TextProcessor
        processor = TextProcessor()
        
        # Extract text using TextProcessor
        extracted_text = processor.extract_text(temp_path, file_extension)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        # Display header for extracted text
        st.write("Extracted Text:")
        
        # Display extracted text in a scrollable text area
        st.text_area("Text", extracted_text, height=300)

# Standard Python idiom to run main function when script is executed
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
# Import os module for operating system interactions and environment variables
import os
# Import load_dotenv function to load environment variables from .env file
from dotenv import load_dotenv

# Load environment variables from .env file into the application's environment
load_dotenv()

class Config:
    """Configuration class to manage application settings and environment variables."""
    
    # Class variable to store GROQ API key from environment
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    @staticmethod
    def validate():
        """Validate that required configuration values are properly set.
        
        Raises:
            ValueError: If GROQ_API_KEY is not set in environment variables
        """
        # Check if GROQ_API_KEY is unset or empty
        if not Config.GROQ_API_KEY:
            # Raise an error if the key is missing
            raise ValueError("GROQ_API_KEY is not set in the .env file")
```

#### **Edit ```lib/groq_handler.py```**
``` python
# Import Groq class from groq library for API interactions
from groq import Groq
# Import Config class from utils.config module for configuration management
from utils.config import Config

class GroqHandler:
    """Class to handle interactions with the Groq API for text analysis."""
    
    def __init__(self):
        """Initialize GroqHandler with validated configuration and API client."""
        # Validate configuration settings
        Config.validate()
        # Create Groq client instance with API key from Config
        self.client = Groq(api_key=Config.GROQ_API_KEY)

    def analyze_text(self, prompt, text, model="gemma2-9b-it", max_tokens=2000):
        """Analyze text using the Groq API with specified prompt and parameters.
        
        Args:
            prompt (str): The instruction or question to guide the analysis
            text (str): The text to analyze
            model (str): The Groq model to use (default: "gemma2-9b-it")
            max_tokens (int): Maximum number of tokens in response (default: 2000)
            
        Returns:
            str: The analyzed text response from the Groq API
        """
        # Send request to Groq API with combined prompt and text
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt + "\n\n" + text}],
            model=model,
            max_tokens=max_tokens
        )
        # Return the stripped content from the first response choice
        return response.choices[0].message.content.strip()
```

#### **Update ```main/app.py```**
``` python
# Import os module for file system operations
import os
# Import sys module for system path modifications
import sys
# Add parent directory to system path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import Streamlit for web application interface
import streamlit as st
# Import TextProcessor for text extraction from files
from lib.text_processor import TextProcessor
# Import GroqHandler for text analysis via Groq API
from lib.groq_handler import GroqHandler

def main():
    """Main function to run the Resume Analyzer web application."""
    # Display application title
    st.title("Resume Analyzer")
    
    # Display subheader for file upload section
    st.subheader("Upload a PDF or Word Resume")
    
    # Create file uploader widget for PDF and DOCX files
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Check if file is uploaded and analyze button is clicked
    if uploaded_file and st.button("Analyze"):
        # Extract file extension from filename
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        # Define temporary file path
        temp_path = f"temp_resume.{file_extension}"
        
        # Save uploaded file temporarily
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Create TextProcessor instance and extract text
        processor = TextProcessor()
        extracted_text = processor.extract_text(temp_path, file_extension)
        
        # Remove temporary file
        os.remove(temp_path)
        
        # Proceed if text was successfully extracted
        if extracted_text:
            # Create GroqHandler instance for analysis
            groq = GroqHandler()
            
            # Define analysis prompt
            prompt = "Analyze this resume text and summarize its key points."
            
            # Show spinner during analysis
            with st.spinner("Analyzing..."):
                # Get analysis from Groq API
                analysis = groq.analyze_text(prompt, extracted_text)
            
            # Display analysis header
            st.write("Analysis:")
            
            # Display analysis in markdown format
            st.markdown(analysis)
        else:
            # Display error if no text was extracted
            st.error("No text extracted from the file.")

# Standard Python idiom to run main function
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
``` python  
# Import os module for operating system interactions and environment variables
import os
# Import load_dotenv function to load environment variables from .env file
from dotenv import load_dotenv

# Load environment variables from .env file into the application's environment
load_dotenv()

class Config:
    """Configuration class to manage application settings and environment variables."""
    
    # Class variable for Groq API key from environment variables
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Class variable defining directory path for log files
    LOG_DIR = "data/logs"
    
    # Class variable defining path to prompts JSON file
    PROMPTS_FILE = "data/prompts.json"

    @staticmethod
    def validate():
        """Validate that required configuration values are properly set.
        
        Raises:
            ValueError: If GROQ_API_KEY is not set in environment variables
        """
        # Check if GROQ_API_KEY is unset or empty
        if not Config.GROQ_API_KEY:
            # Raise an error if the API key is missing
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
# Import json module for JSON file parsing
import json
# Import os module for operating system interactions
import os

class PromptLoader:
    """Class to load and manage prompt templates from a JSON file."""
    
    def __init__(self, prompts_file):
        """Initialize PromptLoader with a prompts file path.
        
        Args:
            prompts_file (str): Path to the JSON file containing prompt templates
        """
        # Store the prompts file path
        self.prompts_file = prompts_file
        # Load prompts during initialization
        self.prompts = self._load_prompts()

    def _load_prompts(self):
        """Load prompt templates from the JSON file.
        
        Returns:
            dict: Dictionary of prompt templates loaded from file
        """
        # Open and read the JSON file with UTF-8 encoding
        with open(self.prompts_file, "r", encoding="utf-8") as f:
            # Parse JSON content into a dictionary
            prompts = json.load(f)
        # Return the loaded prompts
        return prompts

    def get_prompt(self, prompt_key, **kwargs):
        """Retrieve and format a specific prompt template.
        
        Args:
            prompt_key (str): Key to identify the desired prompt in the JSON
            **kwargs: Keyword arguments to format the prompt template
            
        Returns:
            str: Formatted prompt string
        """
        # Get the template string from prompts dictionary
        template = self.prompts[prompt_key]["template"]
        # Format the template with provided keyword arguments
        return template.format(**kwargs)
```

#### **Edit ```lib/resume_analyzer.py```**
``` python
class ResumeAnalyzer:
    """Class to analyze resume text using Groq API and prompt templates."""
    
    def __init__(self, groq_handler, prompt_loader):
        """Initialize ResumeAnalyzer with Groq handler and prompt loader.
        
        Args:
            groq_handler: Instance of GroqHandler for API interactions
            prompt_loader: Instance of PromptLoader for prompt management
        """
        # Store Groq handler instance
        self.grok = groq_handler
        # Store prompt loader instance
        self.prompt_loader = prompt_loader

    def analyze_resume(self, text, designation, experience, domain):
        """Analyze resume text based on specified parameters.
        
        Args:
            text (str): Resume text to analyze
            designation (str): Target job designation
            experience (str): Expected experience level
            domain (str): Industry or domain context
            
        Returns:
            str: Analysis result from Groq API
        """
        # Get formatted prompt using prompt loader
        prompt = self.prompt_loader.get_prompt(
            "resume_analysis",
            designation=designation,
            experience=experience,
            domain=domain
        )
        # Analyze text using Groq handler with prompt and text
        result = self.grok.analyze_text(prompt, text, max_tokens=1500)
        # Return the analysis result
        return result
```

#### **Update ```main/app.py```**
``` python 
# Import sys module for system path modifications
import sys
# Import os module for file system operations
import os
# Import Streamlit for web application interface
import streamlit as st
# Add parent directory to system path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import GroqHandler for API interactions
from lib.groq_handler import GroqHandler
# Import TextProcessor for text extraction
from lib.text_processor import TextProcessor
# Import ResumeAnalyzer for resume analysis
from lib.resume_analyzer import ResumeAnalyzer
# Import Config for configuration settings
from utils.config import Config
# Import PromptLoader for prompt management
from utils.prompt_loader import PromptLoader

def main():
    """Main function to run the Resume Analyzer web application."""
    # Display application title
    st.title("Resume Analyzer")
    
    # Display subheader for file upload section
    st.subheader("Upload a PDF or Word Resume")
    
    # Create file uploader widget for PDF and DOCX files
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Create three columns for input selections
    col1, col2, col3 = st.columns(3)
    
    # Designation selection in first column
    with col1:
        designation = st.selectbox("Select Desired Designation", 
                                 ["Data Scientist", "Data Analyst", "MLOps Engineer", 
                                  "Machine Learning Engineer"])
    
    # Experience level selection in second column
    with col2:
        experience = st.selectbox("Select Experience Level", 
                                ["Fresher", "<1 Year Experience", "1-2 Years Experience", 
                                 "2-5 Years Experience", "5-8 Years Experience", 
                                 "8-10 Years Experience"])
    
    # Domain selection in third column
    with col3:
        domain = st.selectbox("Select Domain", 
                            ["Finance", "Healthcare", "Automobile", "Real Estate"])
    
    # Check if file is uploaded and analyze button is clicked
    if uploaded_file and st.button("Analyze"):
        # Extract file extension from filename
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        # Define temporary file path
        temp_path = f"temp_resume.{file_extension}"
        
        # Save uploaded file temporarily
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Create TextProcessor instance and extract text
        text_processor = TextProcessor()
        extracted_text = text_processor.extract_text(temp_path, file_extension)
        
        # Remove temporary file
        os.remove(temp_path)
        
        # Proceed if text was extracted successfully
        if extracted_text:
            # Initialize GroqHandler for API calls
            grok_handler = GroqHandler()
            
            # Initialize PromptLoader with prompts file from Config
            prompt_loader = PromptLoader(Config.PROMPTS_FILE)
            
            # Initialize ResumeAnalyzer with handlers
            resume_analyzer = ResumeAnalyzer(grok_handler, prompt_loader)
            
            # Show spinner during analysis
            with st.spinner("Analyzing resume... Please wait"):
                # Analyze resume with selected parameters
                analysis = resume_analyzer.analyze_resume(extracted_text, 
                                                        designation, experience, domain)
            
            # Display analysis header
            st.markdown("# Resume Analysis")
            
            # Display analysis result
            st.write(analysis)
        else:
            # Display error if text extraction failed
            st.error("Could not extract text.")

# Standard Python idiom to run main function
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
# Import logging module for application logging
import logging
# Import os module for file system operations
import os

def setup_logger(name, log_file, level=logging.DEBUG):
    """Set up and configure a logger with console and file handlers.
    
    Args:
        name (str): Name of the logger
        log_file (str): Path to the log file
        level (int): Logging level (default: logging.DEBUG)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create a logger instance with the specified name
    logger = logging.getLogger(name)
    
    # Set the logging level for the logger
    logger.setLevel(level)
    
    # Create the directory for the log file if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Create a console handler for logging to stdout
    console_handler = logging.StreamHandler()
    # Set the logging level for console output
    console_handler.setLevel(level)
    
    # Create a file handler for logging to the specified file
    file_handler = logging.FileHandler(log_file)
    # Set the logging level for file output
    file_handler.setLevel(level)
    
    # Define the log message format with timestamp, name, level, and message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Apply the formatter to both handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger only if they haven't been added yet
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    # Return the configured logger
    return logger
```

#### **Update ```lib/text_processor.py```**
``` python
# Import PyMuPDF library for PDF processing
import fitz
# Import Document class from python-docx for Word document processing
from docx import Document

class TextProcessor:
    """Class to process and extract text from PDF and DOCX files with logging."""
    
    def __init__(self, logger):
        """Initialize TextProcessor with a logger instance.
        
        Args:
            logger (logging.Logger): Logger instance for logging operations
        """
        # Store the logger instance
        self.logger = logger

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file with logging.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text from all pages
            
        Raises:
            Exception: If text extraction fails
        """
        # Log the start of PDF text extraction
        self.logger.debug("Extracting text from PDF: %s", pdf_path)
        try:
            # Open the PDF file
            doc = fitz.open(pdf_path)
            # Extract text from each page and join with newlines
            text = "\n".join([page.get_text("text") for page in doc])
            # Close the document
            doc.close()
            # Log successful extraction
            self.logger.debug("Text extracted from PDF: %s", pdf_path)
            return text
        except Exception as e:
            # Log error if extraction fails
            self.logger.error("Error extracting text from PDF %s: %s", pdf_path, str(e))
            # Raise exception with error message
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def extract_text_from_docx(self, docx_path):
        """Extract text from a DOCX file with logging.
        
        Args:
            docx_path (str): Path to the DOCX file
            
        Returns:
            str: Extracted text from all paragraphs
            
        Raises:
            Exception: If text extraction fails
        """
        # Log the start of DOCX text extraction
        self.logger.debug("Extracting text from DOCX: %s", docx_path)
        try:
            # Open the Word document
            doc = Document(docx_path)
            # Extract text from each paragraph and join with newlines
            text = "\n".join([para.text for para in doc.paragraphs])
            # Log successful extraction
            self.logger.debug("Text extracted from DOCX: %s", docx_path)
            return text
        except Exception as e:
            # Log error if extraction fails
            self.logger.error("Error extracting text from DOCX %s: %s", docx_path, str(e))
            # Raise exception with error message
            raise Exception(f"Error extracting text from DOCX: {str(e)}")

    def extract_text(self, file_path, file_extension):
        """Extract text based on file extension with logging.
        
        Args:
            file_path (str): Path to the file
            file_extension (str): File extension ('pdf' or 'docx')
            
        Returns:
            str: Extracted text or empty string if extension not supported
        """
        # Log the start of text extraction
        self.logger.debug("Extracting text from file: %s", file_path)
        # Handle PDF files
        if file_extension == "pdf":
            return self.extract_text_from_pdf(file_path)
        # Handle DOCX files
        elif file_extension == "docx":
            return self.extract_text_from_docx(file_path)
        # Log warning for unsupported extensions
        self.logger.warning("Unsupported file extension: %s", file_extension)
        # Return empty string for unsupported files
        return ""
```

#### **Update ```lib/groq_handler.py```**
``` python
# Import Groq class from groq library for API interactions
from groq import Groq
# Import Config class from utils.config for configuration management
from utils.config import Config

class GroqHandler:
    """Class to handle interactions with the Groq API."""
    
    def __init__(self, logger, prompt_loader):
        """Initialize GroqHandler with logger and prompt loader.
        
        Args:
            logger (logging.Logger): Logger instance for logging operations
            prompt_loader (PromptLoader): Instance for managing prompt templates
            
        Raises:
            ValueError: If Groq client initialization fails
        """
        # Store logger and prompt loader instances
        self.logger = logger
        self.prompt_loader = prompt_loader
        
        # Log initialization start
        self.logger.debug("Initializing GroqHandler")
        try:
            # Validate configuration settings
            Config.validate()
            # Initialize Groq client with API key
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            # Log successful initialization
            self.logger.debug("GroqHandler initialized successfully")
        except Exception as e:
            # Log error and raise exception if initialization fails
            self.logger.error("Error initializing Groq client: %s", str(e))
            raise ValueError(f"Error initializing Groq client: {str(e)}")

    def analyze_text(self, prompt, text, model="gemma2-9b-it", max_tokens=2000, temperature=0):
        """Analyze text using the Groq API, handling large texts by chunking.
        
        Args:
            prompt (str): Instruction or question to guide the analysis
            text (str): Text to analyze
            model (str): Groq model to use (default: "gemma2-9b-it")
            max_tokens (int): Maximum tokens in response (default: 2000)
            temperature (float): Sampling temperature (default: 0)
            
        Returns:
            str: Analyzed text response from Groq API
            
        Raises:
            Exception: If text processing fails
        """
        # Log start of text analysis with parameters
        self.logger.debug("Starting text analysis with model: %s, max_tokens: %d", model, max_tokens)
        try:
            # Define maximum chunk size for processing
            max_length = 3000
            # Split text into chunks if longer than max_length
            chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]
            partial_responses = []
            
            # Process each chunk
            for i, chunk in enumerate(chunks):
                self.logger.debug("Processing chunk %d of %d", i + 1, len(chunks))
                # Send API request for current chunk
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt + "\n\n" + chunk}],
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                # Store response content
                partial_responses.append(response.choices[0].message.content.strip())
                self.logger.debug("Chunk %d processed", i + 1)
            
            # Handle multiple chunks by combining responses
            if len(partial_responses) > 1:
                self.logger.debug("Combining %d partial responses", len(partial_responses))
                # Get prompt for combining responses
                combine_prompt = self.prompt_loader.get_prompt("combine_partial_responses")
                combined_text = "\n\n".join(partial_responses)
                # Send API request to combine partial responses
                final_response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": combine_prompt + "\n\n" + combined_text}],
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                result = final_response.choices[0].message.content.strip()
            else:
                # Use single response if only one chunk
                result = partial_responses[0]
            
            # Log completion of analysis
            self.logger.debug("Text analysis completed")
            return result
        except Exception as e:
            # Log error and raise exception if processing fails
            self.logger.error("Error processing text with Groq API: %s", str(e))
            raise Exception(f"Error processing text with Groq API: {str(e)}")
``` 

#### **Update ```lib/resume_analyzer.py```**
``` python
class ResumeAnalyzer:
    """Class to analyze resumes using GroqHandler."""
    
    def __init__(self, groq_handler, logger, prompt_loader):
        """Initialize ResumeAnalyzer with required components.
        
        Args:
            groq_handler (GroqHandler): Instance for Groq API interactions
            logger (logging.Logger): Logger instance for logging operations
            prompt_loader (PromptLoader): Instance for managing prompt templates
        """
        # Store Groq handler instance
        self.grok = groq_handler
        # Store logger instance
        self.logger = logger
        # Store prompt loader instance
        self.prompt_loader = prompt_loader

    def analyze_resume(self, text, designation, experience, domain):
        """Analyze resume text based on specified parameters.
        
        Args:
            text (str): Resume text to analyze
            designation (str): Target job designation
            experience (str): Expected experience level
            domain (str): Industry or domain context
            
        Returns:
            str: Analysis result from Groq API
            
        Raises:
            Exception: If analysis fails
        """
        # Log start of resume analysis with parameters
        self.logger.debug("Starting resume analysis for designation: %s, experience: %s, domain: %s",
                         designation, experience, domain)
        try:
            # Get formatted prompt using prompt loader
            prompt = self.prompt_loader.get_prompt(
                "resume_analysis",
                designation=designation,
                experience=experience,
                domain=domain
            )
            # Analyze text using Groq handler
            result = self.grok.analyze_text(prompt, text, max_tokens=1500)
            # Log successful completion
            self.logger.debug("Resume analysis completed")
            return result
        except Exception as e:
            # Log error and raise exception if analysis fails
            self.logger.error("Error analyzing resume: %s", str(e))
            raise Exception(f"Error analyzing resume: {str(e)}")
```

#### **Update ```utils/prompt_loader.py```**
``` python
# Import json module for JSON file parsing
import json
# Import os module for file system operations
import os

class PromptLoader:
    """Class to load and format prompts from a JSON file."""
    
    def __init__(self, prompts_file, logger):
        """Initialize PromptLoader with prompts file and logger.
        
        Args:
            prompts_file (str): Path to the JSON file containing prompts
            logger (logging.Logger): Logger instance for logging operations
        """
        # Store logger instance
        self.logger = logger
        # Store prompts file path
        self.prompts_file = prompts_file
        # Load prompts during initialization
        self.prompts = self._load_prompts()

    def _load_prompts(self):
        """Load prompts from the JSON file.
        
        Returns:
            dict: Dictionary of prompt templates
            
        Raises:
            FileNotFoundError: If prompts file doesn't exist
            Exception: If loading fails for other reasons
        """
        try:
            # Log start of prompt loading
            self.logger.debug("Loading prompts from %s", self.prompts_file)
            # Check if file exists
            if not os.path.exists(self.prompts_file):
                self.logger.error("Prompts file not found: %s", self.prompts_file)
                raise FileNotFoundError(f"Prompts file not found: {self.prompts_file}")
            # Open and read JSON file
            with open(self.prompts_file, "r", encoding="utf-8") as f:
                prompts = json.load(f)
            # Log successful loading
            self.logger.debug("Prompts loaded successfully")
            return prompts
        except Exception as e:
            # Log error and raise exception
            self.logger.error("Error loading prompts: %s", str(e))
            raise Exception(f"Error loading prompts: {str(e)}")

    def get_prompt(self, prompt_key, **kwargs):
        """Fetch and format a prompt by key with provided variables.
        
        Args:
            prompt_key (str): Key to identify the prompt in the JSON
            **kwargs: Keyword arguments for formatting the prompt
            
        Returns:
            str: Formatted prompt string
            
        Raises:
            KeyError: If prompt key is not found
            Exception: If formatting fails
        """
        try:
            # Check if prompt key exists
            if prompt_key not in self.prompts:
                self.logger.error("Prompt key not found: %s", prompt_key)
                raise KeyError(f"Prompt key not found: {prompt_key}")
            # Get template from prompts dictionary
            template = self.prompts[prompt_key]["template"]
            # Format template with provided arguments
            formatted_prompt = template.format(**kwargs)
            # Log successful formatting
            self.logger.debug("Prompt fetched and formatted for key: %s", prompt_key)
            return formatted_prompt
        except Exception as e:
            # Log error and raise exception
            self.logger.error("Error formatting prompt %s: %s", prompt_key, str(e))
            raise Exception(f"Error formatting prompt {prompt_key}: {str(e)}")
```

#### **Update ```main/app.py```**
``` python
# Import sys module for system path modifications
import sys
# Import os module for file system operations
import os
# Import Streamlit for web application interface
import streamlit as st

# Add the project root directory to sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import custom classes from respective modules
from lib.groq_handler import GroqHandler
from lib.text_processor import TextProcessor
from lib.resume_analyzer import ResumeAnalyzer
from utils.config import Config
from utils.logger import setup_logger
from utils.prompt_loader import PromptLoader

# Singleton logger setup (runs only once during session)
if 'loggers' not in st.session_state:
    # Validate configuration settings once
    Config.validate()
    # Initialize loggers dictionary in session state
    st.session_state.loggers = {
        "app": setup_logger("app", f"{Config.LOG_DIR}/app.log"),
        "groq_handler": setup_logger("groq_handler", f"{Config.LOG_DIR}/groq_handler.log"),
        "prompt_loader": setup_logger("prompt_loader", f"{Config.LOG_DIR}/prompt_loader.log"),
        "resume_analyzer": setup_logger("resume_analyzer", f"{Config.LOG_DIR}/resume_analyzer.log"),
        "text_processor": setup_logger("text_processor", f"{Config.LOG_DIR}/text_processor.log")
    }
    # Log application start
    st.session_state.loggers["app"].debug("Starting Resume Analyzer application")

# Reference to loggers from session state
loggers = st.session_state.loggers

def main():
    """Main function to run the Streamlit Resume Analyzer app."""
    # Display application title
    st.title("Resume Analyzer")
    
    # Display subheader for file upload section
    st.subheader("Upload a PDF or Word Resume")
    
    # Create file uploader widget for PDF and DOCX files
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Create three columns for input selections
    col1, col2, col3 = st.columns(3)
    
    # Designation selection dropdown in first column
    with col1:
        designation = st.selectbox("Select Desired Designation", 
                                 ["Data Scientist", "Data Analyst", "MLOps Engineer", 
                                  "Machine Learning Engineer"])
    
    # Experience level selection dropdown in second column
    with col2:
        experience = st.selectbox("Select Experience Level", 
                                ["Fresher", "<1 Year Experience", "1-2 Years Experience", 
                                 "2-5 Years Experience", "5-8 Years Experience", 
                                 "8-10 Years Experience"])
    
    # Domain selection dropdown in third column
    with col3:
        domain = st.selectbox("Select Domain", 
                            ["Finance", "Healthcare", "Automobile", "Real Estate"])
    
    # Process when analyze button is clicked and file is uploaded
    if st.button("Analyze") and uploaded_file:
        # Log user action
        loggers["app"].debug("User clicked Analyze button for file: %s", uploaded_file.name)
        # Extract file extension
        file_extension = uploaded_file.name.split(".")[-1].lower()
        # Define temporary file path
        temp_path = f"temp_resume.{file_extension}"
        try:
            # Save uploaded file temporarily
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Initialize TextProcessor with its logger
            text_processor = TextProcessor(loggers["text_processor"])
            # Extract text from file
            extracted_text = text_processor.extract_text(temp_path, file_extension)
            # Remove temporary file
            os.remove(temp_path)
            
            # Proceed if text was extracted
            if extracted_text:
                # Initialize GroqHandler with its logger and prompt loader
                grok_handler = GroqHandler(loggers["groq_handler"], 
                                         PromptLoader(Config.PROMPTS_FILE, loggers["prompt_loader"]))
                # Initialize ResumeAnalyzer with its components
                resume_analyzer = ResumeAnalyzer(grok_handler, loggers["resume_analyzer"], 
                                               PromptLoader(Config.PROMPTS_FILE, loggers["prompt_loader"]))
                # Show spinner during analysis
                with st.spinner("Analyzing resume... Please wait"):
                    # Perform resume analysis
                    analysis = resume_analyzer.analyze_resume(extracted_text, designation, 
                                                            experience, domain)
                # Display analysis results
                st.markdown("# Resume Analysis")
                st.write(analysis)
            else:
                # Display and log error if text extraction fails
                st.error("Could not extract text.")
                loggers["app"].error("Failed to extract text from %s", uploaded_file.name)
        except Exception as e:
            # Log and display any processing errors
            loggers["app"].error("Error processing resume: %s", str(e))
            st.error(f"Error processing resume: {str(e)}")
            # Clean up temporary file if it exists
            if os.path.exists(temp_path):
                os.remove(temp_path)

# Standard Python idiom to run main function
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
# Import os module for file system operations
import os

def save_text_to_file(text, output_path):
    """Save text to a file with UTF-8 encoding.
    
    Args:
        text (str): Text content to save
        output_path (str): Path where the file will be saved
    """
    # Open file in write mode with UTF-8 encoding
    with open(output_path, "w", encoding="utf-8") as file:
        # Write text to the file
        file.write(text)

def remove_file(file_path):
    """Remove a file if it exists.
    
    Args:
        file_path (str): Path to the file to be removed
    """
    # Check if the file exists
    if os.path.exists(file_path):
        # Remove the file if it exists
        os.remove(file_path)
```

#### **Update ```main/app.py```**
``` python
# Import sys module for system path modifications
import sys
# Import os module for file system operations
import os
# Import Streamlit for web application interface
import streamlit as st

# Add the project root directory to sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import custom classes and utilities from respective modules
from lib.groq_handler import GroqHandler
from lib.text_processor import TextProcessor
from lib.resume_analyzer import ResumeAnalyzer
from utils.file_utils import save_text_to_file, remove_file
from utils.logger import setup_logger
from utils.config import Config
from utils.prompt_loader import PromptLoader

# Singleton logger setup (runs only once during session)
if 'loggers' not in st.session_state:
    # Validate configuration settings once
    Config.validate()
    # Initialize loggers dictionary in session state
    st.session_state.loggers = {
        "app": setup_logger("app", f"{Config.LOG_DIR}/app.log"),
        "groq_handler": setup_logger("groq_handler", f"{Config.LOG_DIR}/groq_handler.log"),
        "prompt_loader": setup_logger("prompt_loader", f"{Config.LOG_DIR}/prompt_loader.log"),
        "resume_analyzer": setup_logger("resume_analyzer", f"{Config.LOG_DIR}/resume_analyzer.log"),
        "text_processor": setup_logger("text_processor", f"{Config.LOG_DIR}/text_processor.log")
    }
    # Log application start
    st.session_state.loggers["app"].debug("Starting Resume Analyzer application")

# Reference to loggers from session state
loggers = st.session_state.loggers

# Cache components to prevent re-initialization
@st.cache_resource
def get_grok_handler():
    """Initialize and cache GroqHandler instance."""
    return GroqHandler(loggers["groq_handler"], PromptLoader(Config.PROMPTS_FILE, loggers["prompt_loader"]))

@st.cache_resource
def get_text_processor():
    """Initialize and cache TextProcessor instance."""
    return TextProcessor(loggers["text_processor"])

@st.cache_resource
def get_resume_analyzer(_grok_handler):
    """Initialize and cache ResumeAnalyzer instance.
    
    Args:
        _grok_handler: Cached GroqHandler instance
    """
    return ResumeAnalyzer(_grok_handler, loggers["resume_analyzer"], PromptLoader(Config.PROMPTS_FILE, loggers["prompt_loader"]))

# Initialize cached components
grok_handler = get_grok_handler()
text_processor = get_text_processor()
resume_analyzer = get_resume_analyzer(grok_handler)

def main():
    """Main function to run the Streamlit Resume Analyzer app."""
    # Initialize session state variables if not present
    if 'page' not in st.session_state:
        st.session_state.page = "upload"
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None
    if 'processed' not in st.session_state:
        st.session_state.processed = False

    # Upload page logic
    if st.session_state.page == "upload":
        st.title("Resume Analyzer")
        st.subheader("Upload a PDF or Word Resume")

        # File uploader widget
        uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
        
        # Create three columns for input selections
        col1, col2, col3 = st.columns(3)
        with col1:
            designation = st.selectbox("Select Desired Designation", 
                                     ["Data Scientist", "Data Analyst", "MLOps Engineer", 
                                      "Machine Learning Engineer"])
        with col2:
            experience = st.selectbox("Select Experience Level", 
                                    ["Fresher", "<1 Year Experience", "1-2 Years Experience", 
                                     "2-5 Years Experience", "5-8 Years Experience", 
                                     "8-10 Years Experience"])
        with col3:
            domain = st.selectbox("Select Domain", 
                                ["Finance", "Healthcare", "Automobile", "Real Estate"])

        # Handle analyze button click
        if st.button("Analyze") and uploaded_file:
            loggers["app"].debug("User clicked Analyze button for file: %s", uploaded_file.name)
            # Store inputs in session state and switch page
            st.session_state.uploaded_file = uploaded_file
            st.session_state.designation = designation
            st.session_state.experience = experience
            st.session_state.domain = domain
            st.session_state.page = "results"
            st.session_state.processed = False
            st.rerun()

    # Results page logic
    elif st.session_state.page == "results":
        uploaded_file = st.session_state.uploaded_file
        file_extension = uploaded_file.name.split(".")[-1].lower()
        temp_path = f"temp_resume.{file_extension}"

        try:
            # Process file only if not already processed
            if not st.session_state.processed:
                loggers["app"].debug("Processing uploaded file: %s", uploaded_file.name)
                # Save uploaded file temporarily
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                # Extract text
                extracted_text = text_processor.extract_text(temp_path, file_extension)
                # Clean up temporary file
                remove_file(temp_path)

                if extracted_text:
                    loggers["app"].debug("Text extracted successfully, length: %d characters", len(extracted_text))
                    with st.spinner("Analyzing resume... Please wait"):
                        # Perform analysis and store in session state
                        st.session_state.analysis = resume_analyzer.analyze_resume(
                            extracted_text, st.session_state.designation, 
                            st.session_state.experience, st.session_state.domain
                        )
                        st.session_state.processed = True
                    loggers["app"].debug("Resume analysis completed")
                else:
                    st.error("Could not extract text. Please check the file format.")
                    loggers["app"].error("Failed to extract text from %s", uploaded_file.name)

            # Display results if analysis exists
            if st.session_state.analysis:
                # Button to return to upload page
                if st.button("Upload New Resume"):
                    loggers["app"].debug("User clicked Upload New Resume")
                    st.session_state.page = "upload"
                    st.session_state.analysis = None
                    st.session_state.processed = False
                    st.rerun()

                # Display analysis
                st.markdown("# Resume Analysis")
                st.write(st.session_state.analysis)

                # Save analysis to file and provide download option
                output_filename = "resume_analysis.txt"
                save_text_to_file(st.session_state.analysis, output_filename)
                with open(output_filename, "rb") as file:
                    st.download_button(label="Download Analysis", data=file, 
                                     file_name=output_filename, mime="text/plain")
                remove_file(output_filename)

        except Exception as e:
            # Handle and log any errors during processing
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