import json

def generate(llm_pipeline, idea, platform, persona=None):
    """Generates a hook, script, and CTA for a given idea."""
    prompt = f"Create a short-form video script for the platform '{platform}'.\n"
    prompt += f"- Video Idea: {idea}\n"
    if persona:
        prompt += f"- Creator Persona: {persona}\n"
    prompt += "The output must be a JSON object with three keys: 'hook', 'script', and 'cta'.\n"
    prompt += "The hook should be one compelling sentence. The script should be a few sentences. The CTA should ask for engagement."

    response = llm_pipeline(prompt, max_length=300)
    generated_text = response[0]['generated_text']
    
    try:
        # The model might not return perfect JSON, so we clean it up
        json_str = generated_text[generated_text.find('{'):generated_text.rfind('}')+1]
        return json.loads(json_str)
    except (json.JSONDecodeError, IndexError):
        return {
            "hook": "Could not generate a hook.",
            "script": generated_text, # Return raw text on failure
            "cta": "Could not generate a CTA."
        }
