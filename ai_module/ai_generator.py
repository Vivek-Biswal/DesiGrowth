import google.generativeai as genai

# Configure API key
genai.configure(api_key="YOUR_API_KEY_HERE")

# Load Gemini model
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
1. Caption
2. 5 marketing hashtags
3. Call-to-action

Make it attractive for social media marketing.
"""

    try:
        response = model.generate_content(prompt)

        text = response.text

        return {
            "caption": text,
            "hashtags": "#sale #discount #localbusiness #offer #festival",
            "cta": "Visit our store today!"
        }

    except Exception as e:
        # fallback if API fails
        return {
            "caption": f"{business} is offering {offer} on {product} this {festival}! Visit us in {location}.",
            "hashtags": "#sale #discount #offer",
            "cta": "Visit our store today!"
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