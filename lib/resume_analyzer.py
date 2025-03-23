class ResumeAnalyzer:
    """Class to analyze resumes using GroqHandler."""
    def __init__(self, groq_handler, prompt_loader):
        self.grok = groq_handler
        self.prompt_loader = prompt_loader

    def analyze_resume(self, text, designation, experience, domain):
        """Analyze resume text."""
        prompt = self.prompt_loader.get_prompt(
            "resume_analysis",
            designation=designation,
            experience=experience,
            domain=domain
        )
        result = self.grok.analyze_text(prompt, text, max_tokens=1500)
        return result