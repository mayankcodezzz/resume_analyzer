from groq import Groq
from utils.config import Config

class GroqHandler:
    """Class to handle interactions with the Groq API."""
    def __init__(self, logger, prompt_loader):
        self.logger = logger
        self.prompt_loader = prompt_loader
        self.logger.debug("Initializing GroqHandler")
        try:
            Config.validate()  # Ensure API key is set
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            self.logger.debug("GroqHandler initialized successfully")
        except Exception as e:
            self.logger.error("Error initializing Groq client: %s", str(e))
            raise ValueError(f"Error initializing Groq client: {str(e)}")

    def analyze_text(self, prompt, text, model="gemma2-9b-it", max_tokens=2000, temperature=0):
        """Analyze text using the Groq API."""
        self.logger.debug("Starting text analysis with model: %s, max_tokens: %d", model, max_tokens)
        try:
            max_length = 3000
            chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]
            partial_responses = []

            for i, chunk in enumerate(chunks):
                self.logger.debug("Processing chunk %d of %d", i + 1, len(chunks))
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt + "\n\n" + chunk}],
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                partial_responses.append(response.choices[0].message.content.strip())
                self.logger.debug("Chunk %d processed", i + 1)

            if len(partial_responses) > 1:
                self.logger.debug("Combining %d partial responses", len(partial_responses))
                combine_prompt = self.prompt_loader.get_prompt("combine_partial_responses")
                combined_text = "\n\n".join(partial_responses)
                final_response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": combine_prompt + "\n\n" + combined_text}],
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                result = final_response.choices[0].message.content.strip()
            else:
                result = partial_responses[0]

            self.logger.debug("Text analysis completed")
            return result
        except Exception as e:
            self.logger.error("Error processing text with Groq API: %s", str(e))
            raise Exception(f"Error processing text with Groq API: {str(e)}")