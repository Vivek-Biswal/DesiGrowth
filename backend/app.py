import sys
import os

# allow backend to access project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from ai_module.ai_generator import generate_marketing_content
from poster_engine.poster_generator import generate_poster

app = Flask(__name__)
CORS(app)

campaign_history = []


@app.route("/")
def home():
    return "DesiGrowth Backend Running"


# Serve generated poster images
@app.route("/poster/<filename>")
def get_poster(filename):
    return send_from_directory("../poster_engine/generated", filename)


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
        ""
    )

    filename = os.path.basename(poster_path)

    # Correct poster URL
    poster_url = f"http://127.0.0.1:5000/poster/{filename}"

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
    import os
    
    port = int(os.environ.get("PORT", 5000))
    
    app.run(
        host="0.0.0.0",
        port=port
    )