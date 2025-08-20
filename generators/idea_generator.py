from serpapi import GoogleSearch
from pexels_api import API
import os
import google.generativeai as genai
import time

def perform_search(api_key, query, num_results=2):
    """Helper function to perform a Google search."""
    try:
        params = {"q": query, "api_key": api_key, "num": num_results}
        search = GoogleSearch(params)
        search_results = search.get_dict()
        links = [{"title": r.get("title"), "link": r.get("link")} for r in search_results.get("organic_results", [])]
        return links
    except Exception as e:
        print(f"--- ERROR during Google Search for '{query}': {e} ---")
        return []

def get_mood_board_images(api_key, query, num_images=3):
    """Fetches images from Pexels to create a visual mood board."""
    try:
        api = API(api_key)
        api.search(query, page=1, results_per_page=num_images)
        photos = api.get_entries()
        return [photo.src['medium'] for photo in photos]
    except Exception as e:
        print(f"--- ERROR during Pexels API call for '{query}': {e} ---")
        return []

def generate_plan_with_visuals(search_api_key, pexels_api_key, niche, tone, audience, plan_type, platform, selected_persona=None):
    """
    Generates ideas/series, finds links, and creates a mood board, tailored to a specific platform and persona.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Determine the number of ideas based on the plan type
        if plan_type == 'Single Idea':
            num_ideas = 1
        elif plan_type == '3-Part Content Series':
            num_ideas = 3
        elif plan_type == 'Monthly Content Theme':
            num_ideas = 5 # For monthly themes, we'll generate 5 content pillars
        
        # Create a dynamic prompt based on the plan type and platform
        prompt = f"You are a creative strategist. Brainstorm a list of {num_ideas} engaging content ideas for a creator."
        if selected_persona:
            prompt += f"\nThe ideas MUST be tailored to this specific audience persona:\n- Persona Name: {selected_persona.get('name')}\n- Profile: {selected_persona.get('profile')}\n- Pain Point: {selected_persona.get('pain_point')}\n- Goal: {selected_persona.get('goal')}"
        
        if plan_type == "Monthly Content Theme":
            prompt += f"\nBrainstorm 5 high-level content pillars for a month-long content theme suitable for {platform}."
        else:
            prompt += f"\nThe ideas must be specifically tailored for the platform: {platform}."
            if plan_type == '3-Part Content Series':
                prompt += "\nThe ideas must build on each other logically."
        
        prompt += f"\nNiche: {niche}\nAudience: {audience}\nTone: {tone}\nProvide only a numbered list of the ideas."
        
        response = model.generate_content(prompt)
        ideas = [line.strip().lstrip('0123456789.-* ') for line in response.text.split('\n') if line.strip()]
        
        results = []
        for idea in ideas:
            time.sleep(1) # Crucial delay to prevent rate limiting
            keyword_prompt = f"Based on the idea '{idea}', generate 3 short search keywords. Provide only keywords, separated by commas."
            keyword_response = model.generate_content(keyword_prompt)
            keywords = [k.strip() for k in keyword_response.text.split(',')]
            primary_keyword = keywords[0] if keywords else idea
            
            results.append({
                "idea": idea,
                "links": {
                    "articles": perform_search(search_api_key, primary_keyword),
                    "youtube": perform_search(search_api_key, f"site:youtube.com {primary_keyword} shorts"),
                    "instagram": perform_search(search_api_key, f"site:instagram.com reel {primary_keyword}"),
                    "reddit": perform_search(search_api_key, f"site:reddit.com {primary_keyword} discussion")
                },
                "images": get_mood_board_images(pexels_api_key, primary_keyword)
            })
        return results
    except Exception as e:
        return [{"idea": f"An AI API error occurred: {e}", "links": {}, "images": []}]

