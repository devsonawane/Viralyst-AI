import google.generativeai as genai

def generate_localized_ideas(niche, audience, tone, language, region):
    """
    Generates content ideas in a specific language, adapted for a local region.
    """
    try:
        print(f"--- Generating localized ideas for {language} in {region} ---")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are a global marketing expert who understands local cultures.
        Your task is to generate 3 content ideas for a creator, tailored to a specific language and region.

        **Creator's Niche:** "{niche}"
        **Target Audience:** "{audience}"
        **Tone:** "{tone}"
        **Target Language:** "{language}"
        **Target Region/Country:** "{region}"

        The ideas must be in {language}.
        Crucially, they must also include relevant cultural references, local slang, or trends specific to {region} to make the content feel authentic.

        Provide only a numbered list of the 3 localized ideas.
        """
        
        response = model.generate_content(prompt)
        return {"ideas_text": response.text}

    except Exception as e:
        print(f"--- ERROR during localized idea generation: {e} ---")
        return {"error": f"An error occurred: {e}"}

def expand_localized_idea(language, region, idea):
    """
    NEW: Takes a single localized idea and expands it with more detail.
    """
    print(f"--- Expanding localized idea in {language}: {idea} ---")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are a local content expert for {region}.
    A creator has a content idea and needs more detail.
    Expand on the following idea, providing a brief, one-paragraph concept or angle for the content.

    **Language:** Your response MUST be in {language}.
    **Idea to Expand:** "{idea}"

    Provide only the detailed, one-paragraph expansion.
    """
    
    try:
        response = model.generate_content(prompt)
        return {"expanded_idea": response.text}
    except Exception as e:
        print(f"--- ERROR during localized idea expansion: {e} ---")
        return {"error": f"An error occurred: {e}"}

