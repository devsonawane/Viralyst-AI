import google.generativeai as genai
import re

def generate_with_ai(idea, platform, persona=None):
    """
    Generates a high-quality script and hashtags using the Gemini AI model.
    """
    # --- THIS IS THE FIX ---
    # Initialize the dictionary with default values BEFORE the try block.
    script_details = {
        'hook': 'Could not parse hook.',
        'script': 'Could not parse script.',
        'cta': 'Could not parse CTA.',
        'hashtags': 'Could not parse hashtags.'
    }
    # ----------------------

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

        # Use re.split to break the text into sections based on the labels
        parts = re.split(r'\*\*(HOOK:|SCRIPT:|CTA:|HASHTAGS:)\*\*', generated_text, flags=re.IGNORECASE)
        
        if len(parts) > 1:
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
        # Now we can safely return an error message in the dictionary
        script_details["error"] = f"An error occurred while generating the AI script: {e}"
        return script_details


def analyze_hook_with_ai(hook):
    """
    Analyzes a hook for virality and provides feedback and alternatives.
    (This function remains the same)
    """
    print(f"--- Analyzing hook: '{hook}' ---")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are a viral marketing expert who specializes in short-form video hooks.
    Analyze the following hook and provide a "Virality Score", constructive feedback, and 3 enhanced alternatives.

    **Hook to Analyze:** "{hook}"

    Structure your response with these exact labels:
    **SCORE:** (A score out of 10)
    **FEEDBACK:** (1-2 sentences of specific advice)
    **ALTERNATIVES:** (A numbered list of 3 stronger hooks)
    """
    
    try:
        response = model.generate_content(prompt)
        analysis_text = response.text
        print(f"--- Raw analysis output: {analysis_text} ---")

        analysis = {}
        score_match = re.search(r'SCORE:(.*?)\n', analysis_text, re.IGNORECASE)
        feedback_match = re.search(r'FEEDBACK:(.*?)\n', analysis_text, re.IGNORECASE)
        alternatives_match = re.search(r'ALTERNATIVES:(.*)', analysis_text, re.DOTALL | re.IGNORECASE)

        analysis['score'] = score_match.group(1).strip() if score_match else "N/A"
        analysis['feedback'] = feedback_match.group(1).strip() if feedback_match else "N/A"
        
        if alternatives_match:
            alts = alternatives_match.group(1).strip()
            analysis['alternatives'] = [alt.strip() for alt in alts.split('\n') if alt.strip()]
        else:
            analysis['alternatives'] = []
            
        return analysis

    except Exception as e:
        print(f"--- ERROR during hook analysis: {e} ---")
        return {"error": f"An error occurred during analysis: {e}"}

