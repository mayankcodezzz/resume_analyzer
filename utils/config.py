import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the application."""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LOG_DIR = "data/logs"
    PROMPTS_FILE = "data/prompts.json"

    @staticmethod
    def validate():
        """Validate that required environment variables are set."""
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in the .env file")