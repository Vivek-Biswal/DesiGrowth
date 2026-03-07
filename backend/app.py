import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from ai_module.ai_generator import generate_marketing_content
from poster_engine.poster_generator import generate_poster

app = Flask(__name__, static_folder="../poster_engine/generated")
CORS(app)

campaign_history = []


@app.route("/")
def home():
    return "DesiGrowth Backend Running"


@app.route("/generate-campaign", methods=["POST"])
@cross_origin()
def generate_campaign():

    data = request.json

    business = data.get("business")
    product = data.get("product")
    offer = data.get("offer")
    festival = data.get("festival")
    location = data.get("location")

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

    poster_path = generate_poster(
        business,
        product,
        offer,
        caption,
        ""
    )

    filename = os.path.basename(poster_path)

    poster_url = f"http://127.0.0.1:5000/{filename}"

    response = {
        "caption": caption,
        "hashtags": hashtags,
        "cta": cta,
        "poster": poster_url
    }

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