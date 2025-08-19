def repurpose(script, original_platform, target_platforms):
    """
    Repurposes content for different platforms using templates.
    """
    repurposed_content = {}
    print(f"--- Repurposing script for platforms: {', '.join(target_platforms)} ---")

    for target_platform in target_platforms:
        header = f"🚀 Repurposed from a {original_platform} script!\n\n"
        
        if "LinkedIn" in target_platform or "Facebook" in target_platform:
            # Format for professional/social platforms
            body = script.replace(". ", ".\n\n") # Add line breaks for readability
            repurposed_text = f"{header}{body}"
        elif "Twitter" in target_platform:
            # Format for a Twitter thread
            repurposed_text = f"1/ Here's a quick breakdown of my latest video topic. (thread)\n\n{script[:200]}..."
        else:
            repurposed_text = f"{header}{script}"

        repurposed_content[target_platform] = repurposed_text
            
    return repurposed_content

