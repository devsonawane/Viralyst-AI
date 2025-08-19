import google.generativeai as genai

def get_suggestions(input_text, suggestion_type):
    """
    Takes a user's basic input and suggests more detailed alternatives.
    suggestion_type can be 'niche' or 'persona'.
    """
    print(f"--- Getting suggestions for {suggestion_type}: {input_text} ---")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if suggestion_type == 'niche':
        prompt = f"""
        You are a market research expert. A content creator has provided a basic niche idea.
        Brainstorm 3 more specific and engaging sub-niches based on their input.

        **Initial Niche:** "{input_text}"

        Provide only a numbered list of the 3 enhanced niche ideas.
        Example: If the input is "Fitness", you might suggest "High-Intensity Interval Training (HIIT) for busy professionals".
        """
    elif suggestion_type == 'persona':
        prompt = f"""
        You are a brand strategist. A content creator has provided a basic description of their persona.
        Brainstorm 3 more detailed and compelling persona descriptions based on their input.

        **Initial Persona:** "{input_text}"

        Provide only a numbered list of the 3 enhanced persona descriptions.
        Example: If the input is "Friendly fitness coach", you might suggest "An energetic and empathetic ex-athlete who makes fitness feel like a team sport."
        """
    else:
        return {"error": "Invalid suggestion type."}
    
    try:
        response = model.generate_content(prompt)
        suggestions = [line.strip().lstrip('0123456789.-* ') for line in response.text.split('\n') if line.strip()]
        return {"suggestions": suggestions}
    except Exception as e:
        print(f"--- ERROR during suggestion generation: {e} ---")
        return {"error": f"An error occurred: {e}"}

