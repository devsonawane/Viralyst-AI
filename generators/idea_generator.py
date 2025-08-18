from serpapi import GoogleSearch
from pexels_api import API
import os
import google.generativeai as genai

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
    """Fetches images from Pexels."""
    try:
        api = API(api_key)
        api.search(query, page=1, results_per_page=num_images)
        photos = api.get_entries()
        return [photo.src['medium'] for photo in photos]
    except Exception as e:
        print(f"--- ERROR during Pexels API call for '{query}': {e} ---")
        return []

def generate_plan_with_visuals(search_api_key, pexels_api_key, niche, tone, audience, plan_type):
    """
    The new core function that generates ideas/series, finds links, and creates a mood board.
    """
    print(f"--- Generating a {plan_type} for niche: {niche} ---")
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    num_ideas = 3 if plan_type == 'Single Idea' else 5
    prompt = f"""
    You are a creative strategist. Brainstorm a list of {num_ideas} engaging content ideas for a creator.
    If the request is for a 'Content Series', the ideas must build on each other logically.
    
    **Niche:** {niche}
    **Audience:** {audience}
    **Tone:** {tone}

    Provide only a numbered list of the ideas.
    """
    response = model.generate_content(prompt)
    ideas = [line.strip().lstrip('0123456789.-* ') for line in response.text.split('\n') if line.strip()]
    
    results = []
    
    for idea in ideas:
        print(f"--- Researching idea: '{idea}' ---")
        
        # --- NEW: AI-Powered Keyword Generation ---
        keyword_prompt = f"Based on the content idea '{idea}', generate 3 short, effective search keywords. Provide only the keywords, separated by commas."
        keyword_response = model.generate_content(keyword_prompt)
        keywords = [k.strip() for k in keyword_response.text.split(',')]
        primary_keyword = keywords[0] if keywords else idea # Use the first keyword for best results
        print(f"--- Generated Keywords for Search: {keywords} ---")
        # -----------------------------------------

        results.append({
            "idea": idea,
            "links": {
                "articles": perform_search(search_api_key, primary_keyword),
                "youtube": perform_search(search_api_key, f"site:youtube.com {primary_keyword} shorts tutorial"),
                "instagram": perform_search(search_api_key, f"site:instagram.com reel {primary_keyword}"),
                "reddit": perform_search(search_api_key, f"site:reddit.com {primary_keyword} tips discussion") # New Reddit Search
            },
            "images": get_mood_board_images(pexels_api_key, primary_keyword)
        })
            
    return results

