"""
Article type detection using OpenAI API.

Checks whether the submitted content is actually a news article
before running the full analysis pipeline.
"""

import os
import httpx
from typing import Tuple


async def is_news_article(title: str, text: str, domain: str = "") -> Tuple[bool, str]:
    """
    Ask OpenAI whether the content is a news article.

    Returns:
        (is_news: bool, reason: str)
    """
    if "canvas" in domain.lower() or "instructure.com" in domain.lower():
        return False, "This isn't a news article, so we can't analyze it."

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        # If no key is configured, let it through rather than blocking everything
        return True, ""

    snippet = text[:300].strip()
    prompt = (
        "You are a strict content classifier. Determine if the following is a published news article "
        "written by a journalist, reporting on real-world events for a news outlet.\n\n"
        "Answer NO if it is any of these: a course page, university portal, Canvas/LMS page, "
        "social media post, product page, forum thread, government form, blog post, Wikipedia article, "
        "YouTube page, Reddit post, or any non-journalistic content.\n\n"
        "Answer YES only if it is clearly a news article from a media outlet.\n\n"
        f"Title: {title}\n\n"
        f"Content snippet: {snippet}\n\n"
        "Respond with exactly one word: YES or NO."
    )

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 5,
                    "temperature": 0,
                },
            )

        if response.status_code != 200:
            return True, ""

        answer = response.json()["choices"][0]["message"]["content"].strip().upper()
        print(f"[article_detector] OpenAI answered: {answer!r}")

        if answer.startswith("NO"):
            return False, "This doesn't appear to be a news article. Veritas AI can only analyze news content."

        return True, ""

    except Exception:
        # On any error, fail open so legitimate articles aren't blocked
        return True, ""
