import google.generativeai as genai

def predict_trend(niche):
    """
    Predicts a plausible future trend for a given niche with a creative twist.
    """
    print(f"--- Predicting future trends for niche: {niche} ---")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # This prompt is designed to be creative and engaging
    prompt = f"""
    You are the "Trend Oracle," an AI with a playful yet insightful ability to predict future viral trends.
    Based on your vast knowledge of internet culture, past trends, and human psychology, predict one plausible, yet unexpected, future trend for the following niche.

    **Niche:** {niche}

    Your prediction should be structured with these exact labels:
    **THE PREDICTION:** (A bold, one-sentence prediction of a trend that could emerge in the next 3-6 months.)
    **THE REASONING:** (A brief, logical explanation for why this trend could happen.)
    **THE CAMPAIGN IDEA:** (A creative campaign idea for a creator in this niche to capitalize on the trend early.)
    """
    
    try:
        response = model.generate_content(prompt)
        return {"prediction_text": response.text}
    except Exception as e:
        print(f"--- ERROR during trend prediction: {e} ---")
        return {"error": f"An error occurred: {e}"}

