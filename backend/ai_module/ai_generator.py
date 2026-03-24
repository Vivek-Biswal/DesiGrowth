import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("⚠️ Gemini API missing — fallback mode")
    client = None
else:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print("❌ Gemini init failed:", e)
        client = None


def generate_marketing_content(data):
    if not client:
        return {
            "caption": f"{data.get('business')} offering {data.get('offer')} on {data.get('product')}",
            "hashtags": "#sale #offer #business #india"
        }

    try:
        prompt = f"""
        Create marketing content:
        Business: {data.get('business')}
        Product: {data.get('product')}
        Offer: {data.get('offer')}
        Festival: {data.get('festival')}
        Location: {data.get('location')}
        """

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        text = response.text

        return {
            "caption": text,
            "hashtags": "#sale #offer #ai #marketing"
        }

    except Exception as e:
        print("AI error:", e)
        return {
            "caption": "Special offer available now!",
            "hashtags": "#sale #offer"
        }