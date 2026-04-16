"""
Article type detection using OpenAI API.

Checks whether the submitted content is actually a news article
before running the full analysis pipeline.
"""

import os
import httpx
from typing import Tuple


async def is_news_article(title: str, text: str) -> Tuple[bool, str]:
    """
    Ask OpenAI whether the content is a news article.

    Returns:
        (is_news: bool, reason: str)
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("[article_detector] No OPENAI_API_KEY found in environment")
        return True, ""

    print(f"[article_detector] Key loaded: {api_key[:8]}...")

    CONTENT_TYPE_MESSAGES = {
        "PRODUCT":      "This isn't a news article — it looks like a product or shopping page.",
        "SOCIAL_MEDIA": "This isn't a news article — it looks like a social media post.",
        "FORUM":        "This isn't a news article — it looks like a forum or discussion thread.",
        "VIDEO":        "This isn't a news article — it looks like a video page.",
        "COURSE":       "This isn't a news article — it looks like a course or educational page.",
        "BLOG":         "This isn't a news article — it looks like a personal blog post.",
        "WIKI":         "This isn't a news article — it looks like a wiki or encyclopedia page.",
        "OTHER":        "This isn't a news article, so we can't analyze it.",
    }

    snippet = text[:300].strip()
    content_line = f"Content snippet: {snippet}\n\n" if snippet else ""
    prompt = (
        "You are a strict content classifier. Determine if the following is a published news article "
        "written by a journalist reporting on real-world events for a news outlet.\n\n"
        "If it IS a news article, respond with exactly: YES\n"
        "If it is NOT a news article, respond with exactly one of these labels that best fits:\n"
        "PRODUCT, SOCIAL_MEDIA, FORUM, VIDEO, COURSE, BLOG, WIKI, OTHER\n\n"
        f"Title: {title}\n\n"
        f"{content_line}"
        "Respond with one word only."
    )

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 10,
                    "temperature": 0,
                },
            )

        if response.status_code != 200:
            return True, ""

        answer = response.json()["choices"][0]["message"]["content"].strip().upper()
        print(f"[article_detector] OpenAI answered: {answer!r}")

        if answer != "YES":
            label = answer if answer in CONTENT_TYPE_MESSAGES else "OTHER"
            return False, CONTENT_TYPE_MESSAGES[label]

        return True, ""

    except Exception as e:
        print(f"[article_detector] Exception: {e}")
        return True, ""
