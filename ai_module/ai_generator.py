import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_marketing_content(business, product, offer, festival, location):

    prompt = f"""
Create a short marketing advertisement.

Business: {business}
Product: {product}
Offer: {offer}
Festival: {festival}
Location: {location}

Generate:
Caption
5 Hashtags
Call to action
"""

    try:
        response = model.generate_content(prompt)

        text = response.text

        return {
            "caption": text,
            "hashtags": "#sale #discount #offer #festival",
            "cta": "Visit our store today!"
        }

    except:
        return {
            "caption": f"{business} is offering {offer} on {product} this {festival}! Visit us in {location}.",
            "hashtags": "#sale #discount #offer",
            "cta": "Visit our store today!"
        }