def repurpose(llm_pipeline, script, original_platform, target_platforms):
    """Repurposes content for different platforms."""
    repurposed_content = {}
    for target_platform in target_platforms:
        prompt = f"You are a social media expert. Adapt the following '{original_platform}' script into a '{target_platform}'.\n"
        prompt += f"Keep the core message but change the format, tone, and add relevant emojis or formatting (like line breaks for LinkedIn or a thread structure for Twitter).\n"
        prompt += f"Original Script: '{script}'\n"
        prompt += f"Provide only the text for the new post."

        response = llm_pipeline(prompt, max_length=400)
        repurposed_content[target_platform] = response[0]['generated_text'].strip()
        
    return repurposed_content
