"""
Article analysis service

Phase 2: Basic credibility scoring based on source reputation
Phase 3: ML model integration for content credibility
"""

from typing import Dict
from .source_credibility import get_source_credibility, get_source_bias
from .coverage import get_coverage_breakdown
from .ml_model import predict_credibility


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

    # 3. ML model content credibility (Phase 3)
    ml_result = predict_credibility(article.title, article.textContent)
    content_score = ml_result['score']

    # 4. Calculate final credibility score (weighted average)
    credibility_score = int((source_cred * 0.6) + (content_score * 0.4))

    # 5. Get coverage breakdown
    coverage = await get_coverage_breakdown(article.title, article.domain)

    return {
        "credibilityScore": credibility_score,
        "biasRating": source_bias,
        "coverage": coverage,
        "domain": article.domain,
        "title": article.title[:100],
        "metadata": {
            "sourceCredibility": source_cred,
            "contentScore": content_score,
            "mlLabel": ml_result['label'],
            "mlConfidence": round(ml_result['confidence'], 2),
            "analyzed": "ml_model",
        }
    }
