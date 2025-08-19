import os
from dotenv import load_dotenv
from generators import idea_generator, script_generator, calendar_generator, analyzer_generator, localization_generator, trend_predictor
from crossposting import repurposer
import google.generativeai as genai

load_dotenv()

class Chatbot:
    def __init__(self):
        # API Key configurations
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key: genai.configure(api_key=self.gemini_api_key)
        self.search_api_key = os.getenv("SERPAPI_API_KEY")
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")

    def generate_content_plan(self, niche, tone, audience, plan_type):
        if not self.search_api_key or not self.pexels_api_key:
            return [{"idea": "ERROR: Search or Pexels API Key is not configured.", "links": {}, "images": []}]
        return idea_generator.generate_plan_with_visuals(
            search_api_key=self.search_api_key,
            pexels_api_key=self.pexels_api_key,
            niche=niche,
            tone=tone,
            audience=audience,
            plan_type=plan_type
        )

    def generate_script(self, idea, platform, persona=None):
        if not self.gemini_api_key: return {"error": "Gemini API Key not configured."}
        return script_generator.generate_with_ai(idea, platform, persona)

    def analyze_hook(self, hook):
        if not self.gemini_api_key: return {"error": "Gemini API Key not configured."}
        return script_generator.analyze_hook_with_ai(hook)

    def repurpose_content(self, script, original_platform, target_platforms):
        return repurposer.repurpose(script, original_platform, target_platforms)

    def generate_content_calendar(self, niche, audience):
        if not self.gemini_api_key: return {"error": "Gemini API Key not configured."}
        return calendar_generator.generate_calendar(niche, audience)

    def analyze_viral_post(self, url):
        if not self.gemini_api_key: return {"error": "Gemini API Key not configured."}
        return analyzer_generator.analyze_post(url)

    def generate_localized_ideas(self, niche, audience, tone, language, region):
        if not self.gemini_api_key: return {"error": "Gemini API Key not configured."}
        return localization_generator.generate_localized_ideas(niche, audience, tone, language, region)

    def predict_future_trend(self, niche):
        if not self.gemini_api_key: return {"error": "Gemini API Key not configured."}
        return trend_predictor.predict_trend(niche)

