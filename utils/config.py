import os  # Operating system interfaces for environment variable access
from dotenv import load_dotenv  # Library to load environment variables from a .env file

# Load environment variables from .env file into the application's environment
load_dotenv()

class Config:
    """Configuration class to manage application settings and environment variables."""
    
    # Static attribute to store the Grok API key retrieved from environment variables
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    @staticmethod
    def validate():
        """Validate that required environment variables are set.
        
        Raises:
            ValueError: If GROQ_API_KEY is not set or is empty
        """
        # Check if GROQ_API_KEY is missing or empty
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in the .env file")