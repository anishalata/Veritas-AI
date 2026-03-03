"""
Source credibility database

Database of news sources with credibility ratings and bias classifications.
Data sourced from Media Bias/Fact Check and similar organizations.
"""

from typing import Tuple

# Source credibility ratings (0-100)
# Based on journalistic standards, fact-checking, transparency
SOURCE_CREDIBILITY = {
    # High credibility (70-95)
    "apnews.com": 92,
    "reuters.com": 91,
    "bbc.com": 89,
    "npr.org": 87,
    "wsj.com": 86,
    "economist.com": 85,
    "nytimes.com": 84,
    "washingtonpost.com": 83,
    "theguardian.com": 82,
    "cnn.com": 78,
    "nbcnews.com": 77,
    "cbsnews.com": 77,
    "abcnews.go.com": 76,
    "usatoday.com": 75,
    "bloomberg.com": 85,
    "politico.com": 76,
    "thehill.com": 74,
    "axios.com": 80,

    # Medium credibility (50-69)
    "foxnews.com": 62,
    "msnbc.com": 65,
    "huffpost.com": 63,
    "buzzfeednews.com": 70,
    "vox.com": 68,
    "slate.com": 66,
    "vice.com": 64,
    "motherjones.com": 61,
    "breitbart.com": 45,
    "dailywire.com": 52,
    "newsmax.com": 48,
    "oann.com": 42,
    "thefederalist.com": 50,

    # Default for unknown sources
    "_default": 60
}

# Source bias classifications
SOURCE_BIAS = {
    # Left-leaning
    "huffpost.com": "Left",
    "motherjones.com": "Left",
    "msnbc.com": "Center-Left",
    "vox.com": "Center-Left",
    "slate.com": "Center-Left",
    "cnn.com": "Center-Left",
    "nytimes.com": "Center-Left",
    "washingtonpost.com": "Center-Left",

    # Center
    "apnews.com": "Center",
    "reuters.com": "Center",
    "bbc.com": "Center",
    "npr.org": "Center",
    "usatoday.com": "Center",
    "axios.com": "Center",
    "bloomberg.com": "Center",
    "economist.com": "Center",

    # Right-leaning
    "wsj.com": "Center-Right",
    "thehill.com": "Center",
    "foxnews.com": "Right",
    "breitbart.com": "Right",
    "dailywire.com": "Right",
    "newsmax.com": "Right",
    "oann.com": "Right",
    "thefederalist.com": "Right",

    # Default
    "_default": "Center"
}


def get_source_credibility(domain: str) -> int:
    """
    Get credibility rating for a news source.

    Args:
        domain: The domain of the news source (e.g., "cnn.com")

    Returns:
        Credibility score (0-100)
    """
    # Normalize domain (remove www., etc.)
    domain = domain.lower().replace("www.", "")

    return SOURCE_CREDIBILITY.get(domain, SOURCE_CREDIBILITY["_default"])


def get_source_bias(domain: str) -> str:
    """
    Get bias classification for a news source.

    Args:
        domain: The domain of the news source

    Returns:
        Bias rating (Left, Center-Left, Center, Center-Right, Right)
    """
    domain = domain.lower().replace("www.", "")

    return SOURCE_BIAS.get(domain, SOURCE_BIAS["_default"])


def get_source_info(domain: str) -> Tuple[int, str]:
    """
    Get both credibility and bias for a source.

    Args:
        domain: The domain of the news source

    Returns:
        Tuple of (credibility_score, bias_rating)
    """
    return (get_source_credibility(domain), get_source_bias(domain))
