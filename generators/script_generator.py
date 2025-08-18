import google.generativeai as genai
import re

def generate_with_ai(idea, platform, persona=None):
    """
    Generates the script. (This function remains the same as our last version).
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are an expert social media scriptwriter...
    (The rest of this prompt is the same as before)
    """
    # (The rest of this function is the same as before)
    try:
        response = model.generate_content(prompt)
        # (Parsing logic remains the same)
        # ...
        return script_details 
    except Exception as e:
        # ...
        return {"error": f"An error occurred: {e}"}


def analyze_hook_with_ai(hook):
    """
    Analyzes a hook for virality and provides feedback and alternatives.
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

        # Parse the analysis
        analysis = {}
        score_match = re.search(r'SCORE:(.*?)\n', analysis_text, re.IGNORECASE)
        feedback_match = re.search(r'FEEDBACK:(.*?)\n', analysis_text, re.IGNORECASE)
        alternatives_match = re.search(r'ALTERNATIVES:(.*)', analysis_text, re.DOTALL | re.IGNORECASE)

        analysis['score'] = score_match.group(1).strip() if score_match else "N/A"
        analysis['feedback'] = feedback_match.group(1).strip() if feedback_match else "N/A"
        
        if alternatives_match:
            # Clean up the list of alternatives
            alts = alternatives_match.group(1).strip()
            analysis['alternatives'] = [alt.strip() for alt in alts.split('\n') if alt.strip()]
        else:
            analysis['alternatives'] = []
            
        return analysis

    except Exception as e:
        print(f"--- ERROR during hook analysis: {e} ---")
        return {"error": f"An error occurred during analysis: {e}"}

