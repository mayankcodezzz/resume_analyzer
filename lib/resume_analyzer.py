class ResumeAnalyzer:
    """Class to analyze resumes using GroqHandler."""
    def __init__(self, groq_handler, logger, prompt_loader):
        self.grok = groq_handler
        self.logger = logger
        self.prompt_loader = prompt_loader

    def analyze_resume(self, text, designation, experience, domain):
        """Analyze resume text."""
        self.logger.debug("Starting resume analysis for designation: %s, experience: %s, domain: %s",
                         designation, experience, domain)
        try:
            prompt = self.prompt_loader.get_prompt(
                "resume_analysis",
                designation=designation,
                experience=experience,
                domain=domain
            )
            result = self.grok.analyze_text(prompt, text, max_tokens=1500)
            self.logger.debug("Resume analysis completed")
            return result
        except Exception as e:
            self.logger.error("Error analyzing resume: %s", str(e))
            raise Exception(f"Error analyzing resume: {str(e)}")