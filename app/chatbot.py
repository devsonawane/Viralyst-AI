# app/chatbot.py
import os
from dotenv import load_dotenv
from generators import idea_generator, script_generator
from crossposting import repurposer
import google.generativeai as genai

load_dotenv()

class Chatbot:
    def __init__(self):
        # Configure the new Gemini API Key
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            print("Gemini API configured successfully.")
        else:
            print("WARNING: GEMINI_API_KEY not found. Script generation will fail.")
        
        # Keep the SerpApi key for searching
        self.search_api_key = os.getenv("SERPAPI_API_KEY")
        if not self.search_api_key:
            print("WARNING: SERPAPI_API_KEY not found. Link searching will fail.")

    def generate_ideas_with_links(self, niche, tone, audience):
        if not self.search_api_key:
            return [{"idea": "ERROR: Search API Key is not configured.", "links": []}]
        return idea_generator.generate_with_references(self.search_api_key, niche, tone, audience)

    def generate_script(self, idea, platform, persona=None):
        """
        This function now uses the powerful Gemini model.
        """
        if not self.gemini_api_key:
            return {"error": "Gemini API Key is not configured. Cannot generate script."}
        return script_generator.generate_with_ai(idea, platform, persona)

    def repurpose_content(self, script, original_platform, target_platforms):
        # The existing template-based repurposer is fast and reliable, so we'll keep it.
        return repurposer.repurpose(script, original_platform, target_platforms)


