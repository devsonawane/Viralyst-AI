# generators/script_generator.py
import json

def generate(idea, platform, persona=None):
    """
    Generates a hook, script, and CTA for a given idea using a template.
    This function no longer requires a local AI model.
    """
    print(f"--- Generating script for idea: '{idea}' on platform: {platform} ---")

    # Create a script using a simple, reliable template
    hook = f"Stop scrolling! Here's everything you need to know about '{idea.split(' for ')[0]}'."

    script_body = f"In this video, we're diving deep into '{idea}'. We'll cover the key points that every beginner should know. First, we'll talk about the basics. Then, we'll explore some common mistakes to avoid."
    if persona:
        script_body += f" We're approaching this from the perspective of {persona}."

    cta = f"What are your biggest questions about this topic? Let me know in the comments below! #hashtags"

    script_details = {
        "hook": hook,
        "script": script_body,
        "cta": cta
    }

    return script_details
