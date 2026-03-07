import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_marketing_content(business, product, offer, festival, location):

    prompt = f"""
    Create a short marketing advertisement for a small local business.

    Business Name: {business}
    Product: {product}
    Offer: {offer}
    Festival: {festival}
    Location: {location}

    Generate:

    Caption:
    A catchy promotional caption.

    Hashtags:
    5 marketing hashtags.

    CTA:
    A short call-to-action encouraging customers to visit or buy.
    """

    response = model.generate_content(prompt)

    text = response.text

    # Basic parsing
    caption = text
    hashtags = "#sale #discount #offer"
    cta = "Visit our store today!"

    return {
        "caption": caption,
        "hashtags": hashtags,
        "cta": cta
    }
if __name__ == "__main__":

    result = generate_marketing_content(
        "Sharma Grocery",
        "Premium Rice",
        "20% OFF",
        "Diwali",
        "Delhi"
    )

    print(result)
