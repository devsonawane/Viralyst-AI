import google.generativeai as genai
import pandas as pd
import io

def generate_calendar(niche, audience):
    """
    Generates a 7-day content calendar using the AIDA framework.
    """
    print(f"--- Generating content calendar for niche: {niche} ---")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are a master content strategist. Your task is to create a 7-day content calendar for a creator.
    The plan should strategically use the AIDA framework (Awareness, Interest, Desire, Action) to build momentum over the week.

    **Creator's Niche:** {niche}
    **Target Audience:** {audience}

    Generate a plan for Day 1 to Day 7. For each day, provide:
    - **Day:** (e.g., Day 1)
    - **Theme:** (e.g., Awareness: The Biggest Myth)
    - **Topic:** (A specific, engaging content idea)
    - **Format:** (e.g., Instagram Reel, Twitter Thread, Blog Post)

    Structure your response clearly for each day.
    """
    
    try:
        response = model.generate_content(prompt)
        
        # --- Create a downloadable CSV file ---
        # We'll parse the AI's text response into a structured format
        lines = response.text.strip().split('\n')
        calendar_data = []
        day_data = {}
        for line in lines:
            if line.startswith('**Day'):
                if day_data:
                    calendar_data.append(day_data)
                day_data = {'Day': line.replace('**', '').strip()}
            elif ':' in line:
                key, value = [x.strip() for x in line.split(':', 1)]
                day_data[key.replace('**', '')] = value
        if day_data:
            calendar_data.append(day_data)
            
        # Convert to a pandas DataFrame for easy CSV conversion
        df = pd.DataFrame(calendar_data)
        
        # Create an in-memory CSV file
        output = io.StringIO()
        df.to_csv(output, index=False)
        csv_data = output.getvalue()
        
        return {"plan_text": response.text, "csv_data": csv_data}

    except Exception as e:
        print(f"--- ERROR during calendar generation: {e} ---")
        return {"error": f"An error occurred: {e}"}

