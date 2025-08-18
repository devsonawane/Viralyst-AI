import google.generativeai as genai
import re

def generate_with_ai(idea, platform, persona=None):
    """
    Generates a high-quality script and hashtags using the Gemini AI model.
    """
    print(f"--- Generating AI script for idea: '{idea}' ---")
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert social media scriptwriter for viral short-form videos.
    Your task is to create a complete script package for the following content idea.

    **Video Idea:** "{idea}"
    **Platform:** {platform}
    **Creator Persona:** "{persona if persona else 'An engaging and knowledgeable creator'}"

    Please generate the following, with each section clearly labeled on a new line:
    **HOOK:**
    **SCRIPT:**
    **CTA:**
    **HASHTAGS:**
    """

    try:
        response = model.generate_content(prompt)
        generated_text = response.text
        print(f"--- Raw AI output: {generated_text} ---")

        # --- Final, Most Robust Parsing Logic ---
        script_details = {
            'hook': 'Could not parse hook.',
            'script': 'Could not parse script.',
            'cta': 'Could not parse CTA.',
            'hashtags': 'Could not parse hashtags.'
        }

        # Use re.split to break the text into sections based on the labels
        # This is the most reliable method
        parts = re.split(r'\*\*(HOOK:|SCRIPT:|CTA:|HASHTAGS:)\*\*', generated_text, flags=re.IGNORECASE)
        
        # The resulting list will be like ['', 'HOOK:', 'content', 'SCRIPT:', 'content', ...]
        if len(parts) > 1:
            # Start from the first label
            i = 1
            while i < len(parts):
                label = parts[i].replace(":", "").strip().lower()
                content = parts[i+1].strip() if (i+1) < len(parts) else ""
                
                if label == 'hook':
                    script_details['hook'] = content
                elif label == 'script':
                    script_details['script'] = content
                elif label == 'cta':
                    script_details['cta'] = content
                elif label == 'hashtags':
                    script_details['hashtags'] = content
                
                i += 2

        return script_details

    except Exception as e:
        print(f"--- ERROR during Gemini API call: {e} ---")
        return {"error": f"An error occurred while generating the AI script: {e}"}

