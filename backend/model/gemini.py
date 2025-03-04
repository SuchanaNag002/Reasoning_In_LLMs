import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiModelWrapper:
    def __init__(self, model):
        self.model = model

    def generate_content(self, prompt, max_retries=3, delay=10):
        """Generate content with retries if a rate-limit error is encountered."""
        attempts = 0
        while attempts < max_retries:
            try:
                return self.model.generate_content(prompt)
            except Exception as e:
                error_msg = str(e).lower()
                # Check for common rate-limit error indicators
                if "429" in error_msg or "resource" in error_msg:
                    attempts += 1
                    print(f"Rate limit encountered (attempt {attempts}/{max_retries}). Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    raise e
        raise Exception("Max retries reached due to rate limiting.")

def init_gemini_model():
    """
    Configure the Gemini API and return a GeminiModelWrapper instance.
    """
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    return GeminiModelWrapper(model)
