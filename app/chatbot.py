import os
from dotenv import load_dotenv
from trend_providers import google_trends, youtube_trends, twitter_trends
from generators import idea_generator, script_generator
from crossposting import repurposer

# For local LLM - no API key needed
# We'll use a simple text generation pipeline as a placeholder
from transformers import pipeline

# Load environment variables
load_dotenv()

class Chatbot:
    """
    The main chatbot class that orchestrates the entire content ideation process.
    """
    def __init__(self):
        # Initialize a simple text generation model from Hugging Face.
        # This runs locally and is free. For better results, a larger model can be used.
        # google/flan-t5-small is a good starting point.
        print("Loading language model...")
        try:
            self.llm = pipeline('text2text-generation', model='google/flan-t5-small')
            print("Language model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Please ensure you have an internet connection to download the model on first run.")
            print("And that you have PyTorch/TensorFlow installed: pip install torch")
            self.llm = None

    def get_trends(self, source='google', keyword='content creation'):
        """Fetches trends from a specified source."""
        if source == 'google':
            return google_trends.fetch_google_trends(keyword)
        elif source == 'youtube':
            return youtube_trends.fetch_youtube_trending()
        elif source == 'twitter':
            return twitter_trends.fetch_twitter_trends(query=keyword)
        return "Unknown trend source."

    def generate_ideas(self, niche, tone, audience, trend_based=False):
        """Generates content ideas based on user inputs."""
        if not self.llm:
            return ["LLM not loaded. Cannot generate ideas."]
            
        trends = []
        if trend_based:
            # Combine trends from multiple sources
            g_trends = google_trends.fetch_google_trends(niche)[:2]
            y_trends = youtube_trends.fetch_youtube_trending()[:2]
            trends = g_trends + y_trends
        
        return idea_generator.generate(self.llm, niche, tone, audience, trends)

    def generate_script(self, idea, platform, persona=None):
        """Generates a hook, script, and CTA for a given idea."""
        if not self.llm:
            return {"error": "LLM not loaded. Cannot generate script."}
            
        return script_generator.generate(self.llm, idea, platform, persona)

    def repurpose_content(self, script, original_platform, target_platforms):
        """Repurposes a script for different social media platforms."""
        if not self.llm:
            return {"error": "LLM not loaded. Cannot repurpose content."}
            
        return repurposer.repurpose(self.llm, script, original_platform, target_platforms)

# Example usage (for testing)
if __name__ == '__main__':
    bot = Chatbot()
    
    # --- Test Idea Generation ---
    niche = "AI for small business owners"
    tone = "educational and slightly humorous"
    audience = "non-technical entrepreneurs"
    ideas = bot.generate_ideas(niche, tone, audience, trend_based=True)
    print("--- Generated Ideas ---")
    for idea in ideas:
        print(f"- {idea}")

    # --- Test Script Generation ---
    if ideas:
        selected_idea = ideas[0]
        print(f"\n--- Generating Script for: '{selected_idea}' ---")
        script_details = bot.generate_script(selected_idea, platform="Instagram Reel")
        print(f"Hook: {script_details.get('hook')}")
        print(f"Script: {script_details.get('script')}")
        print(f"CTA: {script_details.get('cta')}")

        # --- Test Cross-Posting ---
        print("\n--- Repurposing for LinkedIn and Twitter ---")
        repurposed_content = bot.repurpose_content(
            script_details.get('script'), 
            original_platform="Instagram Reel",
            target_platforms=["LinkedIn Post", "Twitter Thread"]
        )
        for platform, content in repurposed_content.items():
            print(f"\n--- {platform} ---")
            print(content)

