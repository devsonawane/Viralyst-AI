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
        'audio': 'Could not parse audio suggestions.'
    }
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
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
        **AUDIO:** (Suggest 2-3 trending audio ideas. For each, describe the VIBE, the GENRE, and give an EXAMPLE of a real, popular song that fits.)
        """
        response = model.generate_content(prompt)
        generated_text = response.text
        
        parts = re.split(r'\*\*(HOOK:|SCRIPT:|CTA:|HASHTAGS:|AUDIO:)\*\*', generated_text, flags=re.IGNORECASE)
        if len(parts) > 1:
            i = 1
            while i < len(parts):
                label = parts[i].replace(":", "").strip().lower()
                content = parts[i+1].strip() if (i+1) < len(parts) else ""
                if label in script_details:
                    script_details[label] = content
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
                if label in analysis:
                    if label == 'alternatives':
                        analysis[label] = [alt.strip() for alt in content.split('\n') if alt.strip()]
                    else:
                        analysis[label] = content
                i += 2
        return analysis
    except Exception as e:
        return {"error": f"An error occurred during analysis: {e}"}

def generate_hook_lab_analysis(niche, tone):
    """
    Runs the Hook Lab to generate, score, and rank multiple hook styles.
    """
    print(f"--- Running Hook Lab for niche: {niche} ---")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    generation_config = genai.types.GenerationConfig(temperature=0.9)
    
    # --- THIS IS THE CHANGE ---
    # The prompt now asks for 5 hooks and the top 2 recommendations.
    prompt = f"""
    You are a master viral hook writer. Your task is to run a "Hook Lab" for a creator.
    
    **Creator's Niche:** {niche}
    **Desired Tone:** {tone}

    1.  **Generate 5 Hooks:** Create 5 distinct hooks across a variety of proven viral styles (e.g., Contrarian, Curiosity Gap, Data-Driven, Personal Story, Problem/Solution).
    2.  **Score Each Hook:** For each of the 5 hooks, provide a "Virality Score" from 1-10 and a one-sentence rationale explaining the score.
    3.  **Select the Top 2:** After analyzing all 5, identify the two strongest hooks and present them as the final recommendation.

    Structure your response with these exact labels:
    **HOOK LAB ANALYSIS:**
    (A list of all 5 hooks with their style, score, and rationale)

    **TOP 2 RECOMMENDATIONS:**
    (A numbered list of the 2 best hooks)
    """
    
    try:
        response = model.generate_content(prompt, generation_config=generation_config)
        
        return {"hook_lab_text": response.text}

    except Exception as e:
        print(f"--- ERROR during Hook Lab generation: {e} ---")
        return {"error": f"An error occurred during Hook Lab analysis: {e}"}

