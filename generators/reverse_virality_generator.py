import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

def reverse_engineer_and_remix(viral_url, user_niche):
    """
    Analyzes a viral post and remixes its format for the user's niche.
    """
    print(f"--- Reverse engineering URL: {viral_url} for niche: {user_niche} ---")
    
    # 1. Scrape the content from the URL (same as our previous analyzer)
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(viral_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('title').get_text() if soup.find('title') else 'No title found'
        paragraphs = soup.find_all('p')
        post_text = ' '.join([p.get_text() for p in paragraphs[:5]])
        
        content_to_analyze = f"Title: {title}\n\nContent: {post_text}"
        
    except Exception as e:
        print(f"--- ERROR during web scraping: {e} ---")
        return {"error": f"Could not fetch content from the URL. It might be protected."}

    # 2. Analyze and Remix with a two-step AI prompt
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are a viral content analyst. Your task is to reverse engineer a successful post and then remix its core strategy for a different niche.

    **Viral Post Content to Analyze:**
    ---
    {content_to_analyze}
    ---

    **Creator's Niche to Adapt For:** {user_niche}

    First, provide a breakdown of the original post with these labels:
    - **Hook Style:** (e.g., Question, Bold Statement, Story)
    - **Cognitive Bias:** (e.g., Scarcity, Social Proof, Curiosity)
    - **CTA Strategy:** (e.g., Open-ended question, Direct command)

    Second, provide 3 "Remix Ideas" that apply this exact same structure and psychology to the creator's niche.
    """
    
    try:
        analysis_response = model.generate_content(prompt)
        return {"analysis_text": analysis_response.text}
    except Exception as e:
        print(f"--- ERROR during reverse virality analysis: {e} ---")
        return {"error": f"An error occurred during AI analysis: {e}"}

