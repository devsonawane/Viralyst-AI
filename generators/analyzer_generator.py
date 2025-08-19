import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

def analyze_post(url):
    """
    Scrapes a URL and uses AI to reverse engineer its success.
    """
    try:
        print(f"--- Analyzing viral post from URL: {url} ---")
        
        # 1. Scrape the content from the URL
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # A simple approach to get the most meaningful text
        title = soup.find('title').get_text() if soup.find('title') else 'No title found'
        paragraphs = soup.find_all('p')
        post_text = ' '.join([p.get_text() for p in paragraphs[:5]]) # Get first 5 paragraphs
        
        content_to_analyze = f"Title: {title}\n\nContent: {post_text}"

        # 2. Analyze the content with AI
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        You are a viral content analyst. A creator has provided the text from a successful online post.
        Your task is to reverse engineer its success.

        **Content to Analyze:**
        ---
        {content_to_analyze}
        ---

        Provide the following breakdown:
        - **Hook Style:** (e.g., Question, Bold Statement, Story)
        - **Psychological Triggers:** (e.g., Scarcity, Social Proof, Curiosity)
        - **Core Message:** (A one-sentence summary)
        - **How to Remix This:** (3 actionable ideas for how a creator in a different niche could adapt this format)
        """
        
        analysis_response = model.generate_content(prompt)
        return {"analysis_text": analysis_response.text}

    except Exception as e:
        print(f"--- ERROR during post analysis: {e} ---")
        return {"error": f"Could not fetch or read content from the URL. It might be protected or a non-standard format."}

