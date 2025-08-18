import os
from dotenv import load_dotenv
from generators import idea_generator, script_generator
import google.generativeai as genai

load_dotenv()

class Chatbot:
    def __init__(self):
        # Configure Gemini API Key
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            print("Gemini API configured.")
        else:
            print("WARNING: GEMINI_API_KEY not found.")
        
        # Configure SerpApi Key for searching
        self.search_api_key = os.getenv("SERPAPI_API_KEY")
        if not self.search_api_key:
            print("WARNING: SERPAPI_API_KEY not found.")
            
        # Configure Pexels API Key for mood boards
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")
        if not self.pexels_api_key:
            print("WARNING: PEXELS_API_KEY not found.")

    def generate_content_plan(self, niche, tone, audience, plan_type):
        """
        Generates either a single idea or a content series, including links and a mood board.
        """
        if not self.search_api_key or not self.pexels_api_key:
            return [{"idea": "ERROR: Search or Pexels API Key is not configured.", "links": [], "images": []}]
        
        return idea_generator.generate_plan_with_visuals(
            search_api_key=self.search_api_key,
            pexels_api_key=self.pexels_api_key,
            niche=niche,
            tone=tone,
            audience=audience,
            plan_type=plan_type
        )

    def generate_script(self, idea, platform, persona=None):
        """
        Generates the script using the Gemini model.
        """
        if not self.gemini_api_key:
            return {"error": "Gemini API Key is not configured."}
        return script_generator.generate_with_ai(idea, platform, persona)

    def analyze_hook(self, hook):
        """
        Analyzes and enhances a hook using the Gemini model.
        """
        if not self.gemini_api_key:
            return {"error": "Gemini API Key is not configured."}
        return script_generator.analyze_hook_with_ai(hook)

    def repurpose_content(self, script, original_platform, target_platforms):
        return repurposer.repurpose(script, original_platform, target_platforms)

