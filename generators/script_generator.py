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

    Please generate the following, with each section clearly labeled:
    
    1.  **HOOK:** A single, powerful sentence (under 10 words).
    2.  **SCRIPT:** A detailed, 3-part script (approx. 150 words) with visual cues in parentheses.
    3.  **CTA (Call to Action):** An engaging question or directive.
    4.  **HASHTAGS:** A list of 5-7 relevant hashtags.
    """

    try:
        response = model.generate_content(prompt)
        generated_text = response.text
        print(f"--- Raw AI output: {generated_text} ---")

        # --- New, More Robust Parsing Logic ---
        script_details = {}
        
        # Use regular expressions to find content after our keywords, ignoring numbers/formatting
        hook_match = re.search(r'HOOK:(.*?)SCRIPT:', generated_text, re.DOTALL | re.IGNORECASE)
        script_match = re.search(r'SCRIPT:(.*?)CTA', generated_text, re.DOTALL | re.IGNORECASE)
        cta_match = re.search(r'CTA \(Call to Action\):(.*?)HASHTAGS:', generated_text, re.DOTALL | re.IGNORECASE)
        hashtags_match = re.search(r'HASHTAGS:(.*)', generated_text, re.DOTALL | re.IGNORECASE)

        script_details['hook'] = hook_match.group(1).strip() if hook_match else "Could not parse hook."
        script_details['script'] = script_match.group(1).strip() if script_match else "Could not parse script."
        script_details['cta'] = cta_match.group(1).strip() if cta_match else "Could not parse CTA."
        script_details['hashtags'] = hashtags_match.group(1).strip() if hashtags_match else "Could not parse hashtags."

        # Fallback for when the AI uses a simple numbered list
        if "Could not parse" in script_details['hook']:
            lines = [line.strip() for line in generated_text.split('\n') if line.strip()]
            if len(lines) >= 4:
                script_details['hook'] = re.sub(r'^\d+\.\s*\*\*HOOK:\*\*\s*', '', lines[0], flags=re.IGNORECASE)
                script_details['script'] = re.sub(r'^\d+\.\s*\*\*SCRIPT:\*\*\s*', '', lines[1], flags=re.IGNORECASE)
                script_details['cta'] = re.sub(r'^\d+\.\s*\*\*CTA \(Call to Action\):\*\*\s*', '', lines[2], flags=re.IGNORECASE)
                script_details['hashtags'] = re.sub(r'^\d+\.\s*\*\*HASHTAGS:\*\*\s*', '', lines[3], flags=re.IGNORECASE)

        return script_details

    except Exception as e:
        print(f"--- ERROR during Gemini API call: {e} ---")
        return {"error": f"An error occurred while generating the AI script: {e}"}

