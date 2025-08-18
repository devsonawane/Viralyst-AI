import google.generativeai as genai
import re

def generate_with_ai(idea, platform, persona=None):
    """
    Generates a high-quality script and hashtags using the Gemini AI model.
    """
    script_details = {
        'hook': 'Could not parse hook.',
        'script': 'Could not parse script.',
        'cta': 'Could not parse CTA.',
        'hashtags': 'Could not parse hashtags.'
    }

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
        script_details["error"] = f"An error occurred while generating the AI script: {e}"
        return script_details


def analyze_hook_with_ai(hook):
    """
    Analyzes a hook for virality and provides feedback and alternatives.
    """
    print(f"--- Analyzing hook: '{hook}' ---")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Increased 'temperature' to encourage more creative and varied responses
    generation_config = genai.types.GenerationConfig(temperature=0.8)
    
    prompt = f"""
    You are a viral marketing expert. Critically evaluate the following hook for a short-form video.
    Your analysis must be honest and the score should vary based on the hook's quality.

    **Hook to Analyze:** "{hook}"

    Provide your analysis with these exact labels on new lines:
    **SCORE:** (A unique score out of 10, like 7/10 or 9/10)
    **FEEDBACK:** (1-2 sentences of specific advice)
    **ALTERNATIVES:** (A numbered list of 3 stronger hooks)
    """
    
    try:
        response = model.generate_content(prompt, generation_config=generation_config)
        analysis_text = response.text
        print(f"--- Raw analysis output: {analysis_text} ---")

        # Switched to the more reliable re.split method for parsing
        analysis = {
            'score': 'N/A',
            'feedback': 'Could not parse feedback.',
            'alternatives': []
        }
        parts = re.split(r'\*\*(SCORE:|FEEDBACK:|ALTERNATIVES:)\*\*', analysis_text, flags=re.IGNORECASE)
        
        if len(parts) > 1:
            i = 1
            while i < len(parts):
                label = parts[i].replace(":", "").strip().lower()
                content = parts[i+1].strip() if (i+1) < len(parts) else ""
                
                if label == 'score':
                    analysis['score'] = content
                elif label == 'feedback':
                    analysis['feedback'] = content
                elif label == 'alternatives':
                    analysis['alternatives'] = [alt.strip() for alt in content.split('\n') if alt.strip()]
                
                i += 2
            
        return analysis

    except Exception as e:
        print(f"--- ERROR during hook analysis: {e} ---")
        return {"error": f"An error occurred during analysis: {e}"}

