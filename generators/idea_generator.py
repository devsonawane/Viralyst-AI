# generators/idea_generator.py
from serpapi import GoogleSearch
import os

# This is a placeholder for a simple, rule-based idea generator.
# In a real-world scenario, you'd call an external LLM API here (like OpenAI or Cohere).
# For this project, we'll create ideas by combining inputs to show the concept.
def generate_with_references(api_key, niche, tone, audience):
    """
    Generates ideas and finds reference links for them.
    """
    print(f"--- Generating ideas for niche: {niche} ---")

    # 1. Generate some basic ideas based on templates
    ideas = [
        f"A {tone} guide to {niche} for beginners",
        f"Why {audience} struggle with {niche} (and how to fix it)",
        f"The top 3 myths about {niche} debunked"
    ]

    results = []

    # 2. For each idea, perform a Google search to find reference links
    for idea in ideas:
        print(f"--- Searching for references for idea: '{idea}' ---")
        try:
            params = {
                "q": idea,
                "api_key": api_key,
                "num": 3 # Get top 3 results
            }
            search = GoogleSearch(params)
            search_results = search.get_dict()

            links = []
            if "organic_results" in search_results:
                for result in search_results["organic_results"]:
                    links.append({
                        "title": result.get("title"),
                        "link": result.get("link")
                    })

            results.append({"idea": idea, "links": links})

        except Exception as e:
            print(f"--- ERROR during Google Search for '{idea}': {e} ---")
            results.append({"idea": idea, "links": [{"title": "Search failed", "link": "#"}]})

    return results
