import snscrape.modules.twitter as sntwitter
import itertools

def fetch_twitter_trends(query, num_tweets=10):
    """
    Scrapes recent popular tweets for a given query using snscrape.
    Note: snscrape's reliability can vary as Twitter/X changes its frontend/API.
    """
    try:
        scraper = sntwitter.TwitterSearchScraper(f'{query} lang:en')
        tweets = itertools.islice(scraper.get_items(), num_tweets)
        # We'll extract hashtags as a proxy for trends
        trends = set()
        for tweet in tweets:
            if tweet.hashtags:
                for ht in tweet.hashtags:
                    trends.add(f"#{ht}")
        return list(trends) if trends else [f"No recent popular hashtags found for '{query}'."]
    except Exception as e:
        print(f"Error fetching Twitter trends: {e}")
        return ["Could not fetch Twitter/X trends."]

