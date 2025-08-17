# app/chatbot.py
import os
from dotenv import load_dotenv
from generators import idea_generator, script_generator
from crossposting import repurposer

load_dotenv()

# We no longer load a model here, making the app lightweight.

class Chatbot:
    def __init__(self):
        # The SerpApi key should be set as an environment variable for security
        self.search_api_key = os.getenv("SERPAPI_API_KEY")
        if not self.search_api_key:
            print("WARNING: SERPAPI_API_KEY not found in environment variables.")

    def generate_ideas_with_links(self, niche, tone, audience):
        """
        This is the new core function. It generates ideas AND finds links.
        """
        if not self.search_api_key:
            return [{"idea": "ERROR: Search API Key is not configured.", "links": []}]

        # The generation logic is now handled entirely in the generator
        return idea_generator.generate_with_references(self.search_api_key, niche, tone, audience)

    def generate_script(self, idea, platform, persona=None):
        return script_generator.generate(idea, platform, persona)

    def repurpose_content(self, script, original_platform, target_platforms):
        return repurposer.repurpose(script, original_platform, target_platforms)
