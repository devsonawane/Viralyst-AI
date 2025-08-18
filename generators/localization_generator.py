import google.generativeai as genai

def generate_localized_ideas(niche, audience, tone, language, region):
    """
    Generates content ideas in a specific language, adapted for a local region.
    """
    print(f"--- Generating localized ideas for {language} in {region} ---")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are a global marketing expert who understands local cultures.
    Your task is to generate 3 content ideas for a creator, tailored to a specific language and region.

    **Creator's Niche:** {niche}
    **Target Audience:** {audience}
    **Tone:** {tone}
    **Target Language:** {language}
    **Target Region/Country:** {region}

    The ideas must be in {language}.
    Crucially, they must also include relevant cultural references, local slang, or trends specific to {region} to make the content feel authentic.

    Provide only a numbered list of the 3 localized ideas.
    """
    
    try:
        response = model.generate_content(prompt)
        return {"ideas_text": response.text}
    except Exception as e:
        print(f"--- ERROR during localized idea generation: {e} ---")
        return {"error": f"An error occurred: {e}"}
