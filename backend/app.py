from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


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

    caption = f"{business} is offering {offer} on {product} for {festival}!"

    response = {
        "caption": caption,
        "hashtags": "#sale #discount #festival",
        "cta": "Visit our store today!",
        "poster": "generated_poster.png"
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
