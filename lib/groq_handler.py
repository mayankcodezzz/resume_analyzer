from groq import Groq  # Groq SDK for interacting with the Groq API
from utils.config import Config  # Custom configuration class for environment settings

class GroqHandler:
    """Handler class for managing interactions with the Groq API."""
    
    def __init__(self):
        """Initialize the GroqHandler with a validated API client.
        
        Raises:
            ValueError: If Config validation fails (e.g., missing API key)
        """
        # Validate configuration settings before proceeding
        Config.validate()
        # Initialize Groq client with the API key from Config
        self.client = Groq(api_key=Config.GROQ_API_KEY)

    def analyze_text(self, prompt, text, model="gemma2-9b-it", max_tokens=2000):
        """Analyze text using the Groq API with a specified prompt and model.
        
        Args:
            prompt (str): The instruction or question to guide the analysis
            text (str): The text content to be analyzed
            model (str): The Groq model to use (default: "gemma2-9b-it")
            max_tokens (int): Maximum number of tokens in the response (default: 2000)
            
        Returns:
            str: The analyzed text response from the Groq API, stripped of leading/trailing whitespace
        """
        # Send a request to the Groq API with the combined prompt and text
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt + "\n\n" + text}],
            model=model,
            max_tokens=max_tokens
        )
        # Extract and return the content from the first response choice
        return response.choices[0].message.content.strip()