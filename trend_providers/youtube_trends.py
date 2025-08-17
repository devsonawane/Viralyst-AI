import yt_dlp

def fetch_youtube_trending(region_code='US', num_videos=5):
    """
    Fetches top trending video titles from YouTube for a specific region.
    This is a simplified example. yt-dlp is powerful but direct scraping
    of the "Trending" page can be complex. This fetches info from a popular channel's videos as a proxy.
    A more robust method would involve parsing the YouTube trending page directly.
    """
    # Using a popular news channel as a proxy for general trending topics
    YDL_OPTS = {
        'playlistend': num_videos,
        'extract_flat': True,
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            # Replace with a URL of a channel that often covers trending topics
            info = ydl.extract_info("https://www.youtube.com/user/TEDtalksDirector", download=False)
            return [video['title'] for video in info.get('entries', []) if video]
    except Exception as e:
        print(f"Error fetching YouTube trends: {e}")
        return ["Could not fetch YouTube trends."]
