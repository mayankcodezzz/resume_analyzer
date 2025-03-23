import json
import os

class PromptLoader:
    """Class to load and format prompts from a JSON file."""
    def __init__(self, prompts_file):
        self.prompts_file = prompts_file
        self.prompts = self._load_prompts()

    def _load_prompts(self):
        """Load prompts from the JSON file."""
        with open(self.prompts_file, "r", encoding="utf-8") as f:
            prompts = json.load(f)
        return prompts

    def get_prompt(self, prompt_key, **kwargs):
        """Fetch and format a prompt by key with provided variables."""
        template = self.prompts[prompt_key]["template"]
        return template.format(**kwargs)