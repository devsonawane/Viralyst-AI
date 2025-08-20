import google.generativeai as genai
import re

def get_suggestions(input_text, suggestion_type, niche=None):
    """
    Takes a user's basic input and suggests more detailed alternatives.
    Now generates structured personas based on the niche.
    """
    print(f"--- Getting suggestions for {suggestion_type} with niche context: {niche} ---")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if suggestion_type == 'niche':
        prompt = f"""
        You are a market research expert. A content creator has provided a basic niche idea.
        Brainstorm 3 more specific and engaging sub-niches based on their input.

        **Initial Niche:** "{input_text}"

        Provide only a numbered list of the 3 enhanced niche ideas.
        """
    elif suggestion_type == 'persona':
        prompt = f"""
        You are a brand strategist. For the niche "{niche}", generate 4 distinct audience personas.
        For each persona, provide these exact details on new lines:
        **Name:** (A relatable name, e.g., "Busy Rahul")
        **Profile:** (A one-sentence description, e.g., "29, IT Professional, wants quick desk-friendly workouts")
        **Pain Point:** (Their primary struggle)
        **Goal:** (What they want to achieve)
        
        Separate each persona with '---'.
        """
    else:
        return {"error": "Invalid suggestion type."}
    
    try:
        response = model.generate_content(prompt)
        
        if suggestion_type == 'niche':
            suggestions = [line.strip().lstrip('0123456789.-* ') for line in response.text.split('\n') if line.strip()]
            return {"suggestions": suggestions}
        
        elif suggestion_type == 'persona':
            # Parse the structured persona text
            personas = []
            persona_blocks = response.text.strip().split('---')
            for block in persona_blocks:
                if not block.strip(): continue
                persona_dict = {}
                for line in block.strip().split('\n'):
                    if ":" in line:
                        key, value = [x.strip() for x in line.split(":", 1)]
                        key = key.replace("**", "").lower().replace(" ", "_")
                        persona_dict[key] = value
                if 'name' in persona_dict: # Ensure the persona was parsed correctly
                    personas.append(persona_dict)
            return {"personas": personas}

    except Exception as e:
        print(f"--- ERROR during suggestion generation: {e} ---")
        return {"error": f"An error occurred: {e}"}

