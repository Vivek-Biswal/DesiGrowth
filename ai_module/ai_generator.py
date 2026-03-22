"""
ai_module/ai_generator.py
-------------------------
Gemini-powered marketing content generator.
Returns caption, hashtags (string), idea, and cta.

The /generate-content route in routes/ai.py parses hashtags into a list.
Member 3 (AI Engine) should extend this module with structured prompts.
"""

import os
import re

from google import genai
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))
MODEL = "gemini-2.0-flash"


def generate_marketing_content(business, product, offer, festival="", location=""):
    """
    Generate marketing content using Gemini.

    Returns:
        {
            "caption":  str  - ad caption
            "hashtags": str  - space-separated hashtags
            "idea":     str  - campaign idea
            "cta":      str  - call to action
        }
    """
    festival_line = f"Festival/Occasion: {festival}" if festival else ""
    location_line = f"Location: {location}" if location else ""

    prompt = f"""You are an expert Indian digital marketing assistant.
Generate marketing content for a small local business.

Business: {business}
Product: {product}
Offer: {offer}
{festival_line}
{location_line}

Respond in this EXACT format (no extra text):
CAPTION: <one engaging ad caption, 1-2 sentences>
HASHTAGS: <exactly 5 relevant hashtags separated by spaces, each starting with #>
IDEA: <one short campaign idea sentence>
CTA: <call to action phrase>"""

    try:
        response = _client.models.generate_content(model=MODEL, contents=prompt)
        text = response.text.strip()

        caption = _extract(text, "CAPTION")
        hashtags = _extract(text, "HASHTAGS")
        idea = _extract(text, "IDEA")
        cta = _extract(text, "CTA")

        # Fallbacks if parsing fails
        if not caption:
            caption = text  # use full response as caption
        if not hashtags:
            hashtags = "#sale #discount #offer #festival #localbusiness"
        if not idea:
            idea = f"Promote {product} with {offer} offer."
        if not cta:
            cta = "Visit our store today!"

        return {"caption": caption, "hashtags": hashtags, "idea": idea, "cta": cta}

    except Exception:
        # Graceful fallback — never crash the API
        fallback_caption = (
            f"{business} is offering {offer} on {product}"
            + (f" this {festival}" if festival else "")
            + (f" in {location}" if location else "")
            + "! Don\u2019t miss out."
        )
        return {
            "caption": fallback_caption,
            "hashtags": "#sale #discount #offer #localbusiness #smallbusiness",
            "idea": f"Run a flash sale on {product} for 3 days.",
            "cta": "Visit our store today!",
        }


def _extract(text: str, key: str) -> str:
    """Extract the value after a KEY: label from the Gemini response."""
    match = re.search(rf"^{key}:\s*(.+)", text, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""
