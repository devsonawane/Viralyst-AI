import google.generativeai as genai
import re

def generate_with_ai(idea, platform, persona=None):
    """
    Generates a high-quality script, hashtags, AND trending audio suggestions.
    """
    script_details = {
        'hook': 'Could not parse hook.',
        'script': 'Could not parse script.',
        'cta': 'Could not parse CTA.',
        'hashtags': 'Could not parse hashtags.',
        'audio': 'Could not parse audio suggestions.' # New field
    }
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # --- PROMPT UPDATE ---
        # Added a new section for Audio Suggestions
        prompt = f"""
        You are an expert social media scriptwriter and a viral trend spotter.
        Your task is to create a complete script package for the following content idea.

        **Video Idea:** "{idea}"
        **Platform:** {platform}
        **Creator Persona:** "{persona if persona else 'An engaging and knowledgeable creator'}"

        Please generate the following, with each section clearly labeled on a new line:
        **HOOK:** (A single, powerful sentence)
        **SCRIPT:** (A detailed, 3-part script with visual cues)
        **CTA:** (An engaging question or directive)
        **HASHTAGS:** (A list of 5-7 relevant hashtags)
        **AUDIO:** (Suggest 2-3 trending audio ideas. For each, describe the VIBE (e.g., Upbeat, Nostalgic), the GENRE (e.g., Lofi Hip-Hop, Pop), and give an EXAMPLE of a real, popular song that fits.)
        """
        response = model.generate_content(prompt)
        generated_text = response.text
        
        # --- PARSING UPDATE ---
        # Added 'audio' to the parsing logic
        parts = re.split(r'\*\*(HOOK:|SCRIPT:|CTA:|HASHTAGS:|AUDIO:)\*\*', generated_text, flags=re.IGNORECASE)
        if len(parts) > 1:
            i = 1
            while i < len(parts):
                label = parts[i].replace(":", "").strip().lower()
                content = parts[i+1].strip() if (i+1) < len(parts) else ""
                if label == 'hook': script_details['hook'] = content
                elif label == 'script': script_details['script'] = content
                elif label == 'cta': script_details['cta'] = content
                elif label == 'hashtags': script_details['hashtags'] = content
                elif label == 'audio': script_details['audio'] = content # New parsing
                i += 2
        return script_details
    except Exception as e:
        script_details["error"] = f"An error occurred while generating the AI script: {e}"
        return script_details

def analyze_hook_with_ai(hook):
    """
    Analyzes a hook for virality and provides feedback and alternatives.
    """
    try:
        print(f"--- Analyzing hook: '{hook}' ---")
        model = genai.GenerativeModel('gemini-1.5-flash')
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
        response = model.generate_content(prompt, generation_config=generation_config)
        analysis_text = response.text
        
        analysis = {'score': 'N/A', 'feedback': 'Could not parse feedback.', 'alternatives': []}
        parts = re.split(r'\*\*(SCORE:|FEEDBACK:|ALTERNATIVES:)\*\*', analysis_text, flags=re.IGNORECASE)
        if len(parts) > 1:
            i = 1
            while i < len(parts):
                label = parts[i].replace(":", "").strip().lower()
                content = parts[i+1].strip() if (i+1) < len(parts) else ""
                if label == 'score': analysis['score'] = content
                elif label == 'feedback': analysis['feedback'] = content
                elif label == 'alternatives': analysis['alternatives'] = [alt.strip() for alt in content.split('\n') if alt.strip()]
                i += 2
        return analysis
    except Exception as e:
        print(f"--- ERROR during hook analysis: {e} ---")
        return {"error": f"An error occurred during analysis: {e}"}

