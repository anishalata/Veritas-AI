"""
Coverage analysis service

Checks how a story is being covered across the political spectrum.
Uses NewsAPI to find similar articles from different sources.
"""

import os
import httpx
from typing import Dict


# Which sources lean which way
LEFT_SOURCES = {"huffpost.com", "motherjones.com", "msnbc.com", "vox.com", "slate.com", "cnn.com", "nytimes.com", "washingtonpost.com", "theguardian.com", "vice.com"}
RIGHT_SOURCES = {"foxnews.com", "breitbart.com", "dailywire.com", "newsmax.com", "oann.com", "thefederalist.com", "nypost.com"}
CENTER_SOURCES = {"apnews.com", "reuters.com", "bbc.com", "npr.org", "usatoday.com", "axios.com", "bloomberg.com", "economist.com", "thehill.com", "politico.com", "nbcnews.com", "cbsnews.com", "abcnews.go.com"}


def classify_source(domain: str) -> str:
    domain = domain.lower().replace("www.", "")
    if domain in LEFT_SOURCES:
        return "left"
    if domain in RIGHT_SOURCES:
        return "right"
    if domain in CENTER_SOURCES:
        return "center"
    return "center"  # default unknown sources to center


async def get_coverage_breakdown(title: str, source_domain: str) -> Dict[str, int]:
    """
    Get coverage breakdown across political spectrum using NewsAPI.

    Args:
        title: Article title to search for
        source_domain: Original source domain

    Returns:
        Dictionary with left, center, right percentages
    """
    api_key = os.getenv("NEWSAPI_KEY")

    if not api_key:
        return {"left": 33, "center": 34, "right": 33}

    # Strip filler words and use up to 10 meaningful words as search query
    stop_words = {"the", "a", "an", "is", "in", "on", "at", "to", "for", "of", "and", "or", "but", "with", "as", "by", "from", "its", "it", "are", "was", "be", "has", "have"}
    meaningful_words = [w for w in title.split() if w.lower() not in stop_words]
    query = " ".join(meaningful_words[:10])

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": query,
                    "language": "en",
                    "pageSize": 20,
                    "sortBy": "relevancy",
                    "apiKey": api_key,
                }
            )

        if response.status_code != 200:
            return _fallback_coverage(source_domain)

        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            return _fallback_coverage(source_domain)

        # Count how many articles came from left/center/right sources
        counts = {"left": 0, "center": 0, "right": 0}

        for article in articles:
            source_url = article.get("url", "")
            # Extract domain from URL
            try:
                domain = source_url.split("/")[2].replace("www.", "")
                lean = classify_source(domain)
                counts[lean] += 1
            except:
                counts["center"] += 1

        total = sum(counts.values())

        if total == 0:
            return _fallback_coverage(source_domain)

        return {
            "left": round((counts["left"] / total) * 100),
            "center": round((counts["center"] / total) * 100),
            "right": round((counts["right"] / total) * 100),
        }

    except Exception:
        return _fallback_coverage(source_domain)


def _fallback_coverage(source_domain: str) -> Dict[str, int]:
    """Returns a basic fallback if NewsAPI fails."""
    from .source_credibility import get_source_bias
    bias = get_source_bias(source_domain)

    if bias == "Left":
        return {"left": 50, "center": 30, "right": 20}
    elif bias == "Right":
        return {"left": 20, "center": 30, "right": 50}
    else:
        return {"left": 30, "center": 40, "right": 30}
