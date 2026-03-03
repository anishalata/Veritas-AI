"""
Coverage analysis service

Checks how a story is being covered across the political spectrum.
Uses NewsAPI to find similar articles from different sources.
"""

import os
from typing import Dict
import random


async def get_coverage_breakdown(title: str, source_domain: str) -> Dict[str, int]:
    """
    Get coverage breakdown across political spectrum.

    Phase 2: Returns simulated data
    Phase 2.5: Will integrate with NewsAPI
    Phase 3: Will add ML for better matching

    Args:
        title: Article title
        source_domain: Original source domain

    Returns:
        Dictionary with left, center, right percentages
    """

    # TODO: Integrate NewsAPI
    # For now, return realistic-looking distribution

    # Simulate coverage based on source bias
    from .source_credibility import get_source_bias

    bias = get_source_bias(source_domain)

    # Generate semi-realistic distribution
    if bias == "Left":
        left = random.randint(40, 60)
        center = random.randint(20, 35)
        right = 100 - left - center
    elif bias == "Right":
        right = random.randint(40, 60)
        center = random.randint(20, 35)
        left = 100 - right - center
    else:  # Center
        center = random.randint(35, 50)
        left = random.randint(20, 35)
        right = 100 - center - left

    return {
        "left": max(0, left),
        "center": max(0, center),
        "right": max(0, right)
    }


# Future: NewsAPI integration
async def search_similar_articles(title: str):
    """
    Search for similar articles using NewsAPI.
    To be implemented in Phase 2.5
    """
    api_key = os.getenv("NEWSAPI_KEY")

    if not api_key:
        return []

    # TODO: Implement NewsAPI search
    # from newsapi import NewsApiClient
    # newsapi = NewsApiClient(api_key=api_key)
    # articles = newsapi.get_everything(q=title, language='en', sort_by='relevancy')
    # return articles

    return []
