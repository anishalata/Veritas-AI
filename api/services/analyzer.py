"""
Article analysis service

Phase 2: Basic credibility scoring based on source reputation
Phase 3: Will add ML model integration
"""

from typing import Dict
import re
from .source_credibility import get_source_credibility, get_source_bias
from .coverage import get_coverage_breakdown


async def analyze_article_content(article) -> Dict:
    """
    Analyze article for credibility, bias, and coverage.

    Args:
        article: ArticleRequest with domain, title, content, etc.

    Returns:
        Dictionary with credibilityScore, biasRating, coverage, etc.
    """

    # 1. Get source credibility from database
    source_cred = get_source_credibility(article.domain)

    # 2. Get source bias
    source_bias = get_source_bias(article.domain)

    # 3. Analyze content (basic for now, ML in Phase 3)
    content_score = analyze_content_credibility(article.textContent, article.title)

    # 4. Calculate final credibility score (weighted average)
    credibility_score = int((source_cred * 0.6) + (content_score * 0.4))

    # 5. Get coverage breakdown (will use NewsAPI in next step)
    coverage = await get_coverage_breakdown(article.title, article.domain)

    return {
        "credibilityScore": credibility_score,
        "biasRating": source_bias,
        "coverage": coverage,
        "domain": article.domain,
        "title": article.title[:100],  # Truncate
        "metadata": {
            "sourceCredibility": source_cred,
            "contentScore": content_score,
            "analyzed": "server",
        }
    }


def analyze_content_credibility(text: str, title: str) -> int:
    """
    Basic content analysis (Phase 2).
    Phase 3 will replace with ML model.

    Checks for:
    - Clickbait indicators
    - All caps words
    - Excessive punctuation
    - Sensational language
    """
    score = 75  # Start with neutral score

    # Check for clickbait patterns
    clickbait_patterns = [
        r"you won't believe",
        r"shocking",
        r"doctors hate",
        r"this one trick",
        r"what happens next will",
    ]

    title_lower = title.lower()
    for pattern in clickbait_patterns:
        if re.search(pattern, title_lower):
            score -= 15
            break

    # Check for excessive caps
    if sum(1 for c in title if c.isupper()) / max(len(title), 1) > 0.3:
        score -= 10

    # Check for excessive punctuation
    if title.count('!') > 2 or title.count('?') > 2:
        score -= 10

    # Ensure score is in valid range
    return max(30, min(95, score))
