from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Try importing AI module
try:
    from ai_module.ai_generator import generate_marketing_content
except:
    def generate_marketing_content(business, product, offer, festival, location):
        return {
            "caption": f"{business} is offering {offer} on {product} for {festival}!",
            "hashtags": "#sale #discount #festival",
            "cta": "Visit our store today!"
        }

# Try importing poster generator
try:
    from poster_engine.poster_generator import generate_poster
except:
    def generate_poster(business, product, offer, caption, image_path):
        return "generated_poster.png"


@app.route("/")
def home():
    return "DesiGrowth Backend Running"


@app.route("/generate-campaign", methods=["POST"])
def generate_campaign():

    data = request.json

    business = data.get("business")
    product = data.get("product")
    offer = data.get("offer")
    festival = data.get("festival")
    location = data.get("location")

    # Generate marketing content
    ai_result = generate_marketing_content(
        business,
        product,
        offer,
        festival,
        location
    )

    caption = ai_result["caption"]
    hashtags = ai_result["hashtags"]
    cta = ai_result["cta"]

    # Generate poster
    poster_path = generate_poster(
        business,
        product,
        offer,
        caption,
        "product.jpg"
    )

    response = {
        "caption": caption,
        "hashtags": hashtags,
        "cta": cta,
        "poster": poster_path
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)