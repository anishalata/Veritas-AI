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
        # If no key is configured, let it through rather than blocking everything
        return True, ""

    snippet = text[:300].strip()
    prompt = (
        "You are a content classifier. Determine if the following is a news article "
        "(reporting on real-world events, with a headline and journalistic content).\n\n"
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

        if answer.startswith("NO"):
            return False, "This doesn't appear to be a news article. Veritas AI can only analyze news content."

        return True, ""

    except Exception:
        # On any error, fail open so legitimate articles aren't blocked
        return True, ""
