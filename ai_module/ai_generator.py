import google.generativeai as genai

genai.configure(api_key="AIzaSyB2HGHX6wTGnarB2ioBeLDxV0mgG9KAFaQ")

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
1 Caption
5 Hashtags
1 Call to action
"""

    try:
        response = model.generate_content(prompt)

        text = response.text

        return {
            "caption": text,
            "hashtags": "#sale #discount #offer #festival #shoplocal",
            "cta": "Visit our store today!"
        }

    except:
        # fallback if AI fails
        return {
            "caption": f"{business} is offering {offer} on {product} this {festival}! Visit us in {location}.",
            "hashtags": "#sale #discount #offer",
            "cta": "Visit our store today!"
        }