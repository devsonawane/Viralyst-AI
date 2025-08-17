def generate(llm_pipeline, niche, tone, audience, trends=None):
    """Generates content ideas using the local LLM."""
    prompt = f"You are a creative content strategist. Generate 3 unique, non-generic content ideas for the following creator:\n"
    prompt += f"- Niche: {niche}\n"
    prompt += f"- Target Audience: {audience}\n"
    prompt += f"- Tone: {tone}\n"
    if trends:
        trend_str = ", ".join(trends)
        prompt += f"- Incorporate these current trends: {trend_str}\n"
    prompt += "Ideas should be short, actionable titles. Output them as a numbered list."
    
    # The pipeline returns a list of dictionaries
    response = llm_pipeline(prompt, max_length=150, num_return_sequences=1)
    generated_text = response[0]['generated_text']
    
    # Simple parsing of the numbered list
    ideas = [line.strip().split('. ', 1)[-1] for line in generated_text.split('\n') if line.strip() and line.strip()[0].isdigit()]
    return ideas if ideas else ["Could not generate ideas. The model might need a more specific prompt."]
