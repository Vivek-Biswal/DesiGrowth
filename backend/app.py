from flask import Flask, request, jsonify
from flask_cors import CORS

# Import AI module
from ai_module.ai_generator import generate_marketing_content

# Import poster generator
from poster_engine.poster_generator import generate_poster

app = Flask(__name__)
CORS(app)

# Store campaign history
campaign_history = []


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

    # Call AI generator
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
        ""
    )

    response = {
        "caption": caption,
        "hashtags": hashtags,
        "cta": cta,
        "poster": poster_path
    }

    # Save campaign to history
    campaign_history.append({
        "business": business,
        "product": product,
        "offer": offer,
        "festival": festival,
        "location": location,
        "caption": caption
    })

    return jsonify(response)


@app.route("/campaign-history", methods=["GET"])
def get_campaign_history():
    return jsonify(campaign_history)


if __name__ == "__main__":
    app.run(debug=True)