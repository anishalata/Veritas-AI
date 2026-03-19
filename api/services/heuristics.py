"""
Heuristic signals for credibility analysis - Phase 4

Analyzes surface-level features of article text to generate
a heuristic credibility score and human-readable reasons.
"""

import re
from typing import Dict, List


SENSATIONAL_WORDS = {
    "shocking", "bombshell", "explosive", "breaking", "urgent", "alert",
    "exposed", "leaked", "outrage", "scandal", "conspiracy", "hoax",
    "terrifying", "horrifying", "unbelievable", "miracle", "secret",
    "they don't want you to know", "wake up", "mainstream media"
}

ATTRIBUTION_PHRASES = [
    "according to", "said", "told reporters", "confirmed", "stated",
    "announced", "reported by", "spokesperson", "official", "expert",
    "researcher", "study", "survey", "data shows", "statistics show"
]


def analyze_heuristics(title: str, text: str) -> Dict:
    """
    Run heuristic analysis on article title and text.

    Returns:
        {
            'score': int (0-100),
            'reasons': list of plain-English explanation strings
        }
    """
    reasons = []
    signals = []

    title_lower = title.lower()
    text_lower = text.lower()
    full_text = title + " " + text

    # --- Signal 1: Sensational language ---
    sensational_hits = [w for w in SENSATIONAL_WORDS if w in title_lower or w in text_lower]
    if len(sensational_hits) >= 3:
        signals.append(-25)
        reasons.append("High sensational language detected (e.g. '" + sensational_hits[0] + "')")
    elif len(sensational_hits) >= 1:
        signals.append(-10)
        reasons.append("Some sensational language detected (e.g. '" + sensational_hits[0] + "')")

    # --- Signal 2: Excessive caps in title ---
    words_in_title = title.split()
    caps_words = [w for w in words_in_title if w.isupper() and len(w) > 2]
    if len(caps_words) >= 3:
        signals.append(-15)
        reasons.append("Title uses excessive ALL CAPS words")
    elif len(caps_words) >= 1:
        signals.append(-5)
        reasons.append("Title contains ALL CAPS emphasis")

    # --- Signal 3: Excessive punctuation in title ---
    exclamations = title.count('!')
    question_marks = title.count('?')
    if exclamations >= 2 or (exclamations >= 1 and question_marks >= 1):
        signals.append(-15)
        reasons.append("Title uses excessive punctuation (!!/?)")
    elif exclamations == 1:
        signals.append(-5)
        reasons.append("Title uses exclamation mark")

    # --- Signal 4: Source attribution (named sources, experts, data) ---
    attribution_count = sum(1 for phrase in ATTRIBUTION_PHRASES if phrase in text_lower)
    if attribution_count >= 5:
        signals.append(20)
        reasons.append("Strong source attribution — cites multiple named sources or experts")
    elif attribution_count >= 2:
        signals.append(10)
        reasons.append("Some source attribution present")
    else:
        signals.append(-10)
        reasons.append("Little to no source attribution found")

    # --- Signal 5: Outbound links / citations ---
    link_count = len(re.findall(r'https?://', text))
    if link_count >= 3:
        signals.append(15)
        reasons.append("Article contains multiple outbound citations or links")
    elif link_count >= 1:
        signals.append(5)
        reasons.append("Article contains at least one outbound link")

    # --- Signal 6: Article length (very short articles are often low quality) ---
    word_count = len(text.split())
    if word_count < 150:
        signals.append(-10)
        reasons.append("Article is very short — limited detail or context")
    elif word_count >= 500:
        signals.append(10)
        reasons.append("Article is detailed and well-developed")

    # Compute heuristic score starting from neutral 50
    raw_score = 50 + sum(signals)
    score = max(10, min(95, raw_score))

    # Only return the top 3 most meaningful reasons
    return {
        "score": score,
        "reasons": reasons[:5]
    }
