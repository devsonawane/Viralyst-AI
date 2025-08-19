import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

def analyze_performance_and_suggest(post_url):
    """
    Analyzes a user's own post and suggests future content.
    """
    print(f"--- Analyzing user's post for feedback: {post_url} ---")
    
    # 1. Scrape the user's post content
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(post_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('title').get_text() if soup.find('title') else 'No title'
        paragraphs = soup.find_all('p')
        post_text = ' '.join([p.get_text() for p in paragraphs[:5]])
        
        content_to_analyze = f"Title: {title}\n\nContent: {post_text}"

    except Exception as e:
        print(f"--- ERROR during web scraping: {e} ---")
        return {"error": f"Could not fetch content from your URL."}

    # 2. Use AI to simulate an expert analysis and provide feedback
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are an expert social media analyst. A creator has shared a link to a piece of content they published.
    Your task is to analyze its content and provide a "Feedback Loop" to help them improve.

    **Creator's Post Content:**
    ---
    {content_to_analyze}
    ---

    Assume this post received moderate engagement (e.g., 1000 likes, 50 comments, 10 shares).
    Provide the following analysis:
    - **What Worked Well:** (Identify 1-2 strengths of the post, like a strong hook or clear value proposition).
    - **Area for Improvement:** (Identify 1-2 weaknesses, like a weak call-to-action or unclear visuals).
    - **Improved Future Content:** (Suggest 3 specific, improved content ideas for their next posts that build on the strengths and fix the weaknesses).
    """
    
    try:
        feedback_response = model.generate_content(prompt)
        return {"feedback_text": feedback_response.text}
    except Exception as e:
        print(f"--- ERROR during feedback loop analysis: {e} ---")
        return {"error": f"An error occurred during AI analysis: {e}"}

