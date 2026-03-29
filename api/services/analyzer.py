"""
Article analysis service - Phase 4

Combines source credibility, ML model, and heuristic signals
into a final score with human-readable explanations.
"""

from typing import Dict
from .source_credibility import get_source_credibility, get_source_bias
from .coverage import get_coverage_breakdown
from .ml_model import predict_credibility
from .heuristics import analyze_heuristics
from .article_detector import is_news_article


async def analyze_article_content(article) -> Dict:
    """
    Analyze article for credibility, bias, and coverage.

    Returns:
        Dictionary with credibilityScore, biasRating, coverage, reasons, etc.
    """

    # 0. Check if content is actually a news article
    is_news, detection_message = await is_news_article(article.title, article.textContent, article.domain)
    if not is_news:
        return {
            "credibilityScore": 0,
            "biasRating": "Unknown",
            "coverage": {"left": 0, "center": 0, "right": 0},
            "domain": article.domain,
            "title": article.title[:100],
            "reasons": [],
            "isNewsArticle": False,
            "detectionMessage": detection_message,
            "metadata": {},
        }

    # 1. Source credibility from database
    source_cred = get_source_credibility(article.domain)

    # 2. Source bias
    source_bias = get_source_bias(article.domain)

    # 3. ML model prediction
    ml_result = predict_credibility(article.title, article.textContent)
    ml_score = ml_result['score']
    ml_label = ml_result['label']
    ml_confidence = ml_result['confidence']

    # 4. Heuristic signals
    heuristic_result = analyze_heuristics(article.title, article.textContent)
    heuristic_score = heuristic_result['score']
    reasons = heuristic_result['reasons']

    # 5. Combine ML + heuristics (70/30 split as per plan)
    content_score = int((ml_score * 0.7) + (heuristic_score * 0.3))

    # 6. Final score: source credibility (60%) + content score (40%)
    final_score = int((source_cred * 0.6) + (content_score * 0.4))

    # 7. Determine label — use "Uncertain" band when model is not confident
    label = "Uncertain" if ml_confidence < 0.55 else ml_label

    # 8. Coverage breakdown
    coverage = await get_coverage_breakdown(article.title, article.domain)

    return {
        "credibilityScore": final_score,
        "biasRating": source_bias,
        "coverage": coverage,
        "domain": article.domain,
        "title": article.title[:100],
        "reasons": reasons,
        "isNewsArticle": True,
        "detectionMessage": "",
        "metadata": {
            "sourceCredibility": source_cred,
            "mlScore": ml_score,
            "heuristicScore": heuristic_score,
            "contentScore": content_score,
            "mlLabel": label,
            "mlConfidence": round(ml_confidence, 2),
        }
    }
