import google.generativeai as genai

genai.configure(api_key="AIzaSyB2HGHX6wTGnarB2ioBeLDxV0mgG9KAFaQ")

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_marketing_content(business, product, offer, festival, location):

    prompt = f"""
    Create a marketing advertisement for a small business.

    Business Name: {business}
    Product: {product}
    Offer: {offer}
    Festival: {festival}
    Location: {location}

    Generate:
    1. Caption
    2. 5 marketing hashtags
    3. Call to action

    Keep it short and attractive for social media marketing.
    """

    response = model.generate_content(prompt)

    text = response.text

    return {
        "caption": text,
        "hashtags": "",
        "cta": ""
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
