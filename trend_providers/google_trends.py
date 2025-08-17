from pytrends.request import TrendReq

def fetch_google_trends(keyword, timeframe='today 1-m', geo='US'):
    """Fetches related rising queries from Google Trends."""
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
        related_queries = pytrends.related_queries()
        rising_queries = related_queries[keyword]['rising']
        if rising_queries is not None and not rising_queries.empty:
            return rising_queries['query'].tolist()
        return ["No rising trends found for this keyword."]
    except Exception as e:
        print(f"Error fetching Google Trends: {e}")
        return [f"Could not fetch Google Trends data for '{keyword}'."]

