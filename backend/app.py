import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
import uuid

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont

# Import AI generator
from ai_module.ai_generator import generate_marketing_content

# Create Flask app FIRST
app = Flask(__name__)
CORS(app)

# Poster folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTER_FOLDER = os.path.join(BASE_DIR, "posters")

os.makedirs(POSTER_FOLDER, exist_ok=True)


# ==============================
# HOME ROUTE
# ==============================

@app.route("/")
def home():
    return "DesiGrowth Backend Running"


# ==============================
# POSTER GENERATOR
# ==============================

def create_poster(business, product, offer):

    width = 800
    height = 800

    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font1 = ImageFont.truetype("arial.ttf", 60)
        font2 = ImageFont.truetype("arial.ttf", 40)
    except:
        font1 = ImageFont.load_default()
        font2 = ImageFont.load_default()

    draw.text((100,100), business, fill="black", font=font1)
    draw.text((100,300), product, fill="blue", font=font2)
    draw.text((100,450), offer, fill="red", font=font2)

    filename = f"poster_{uuid.uuid4().hex}.png"
    path = os.path.join(POSTER_FOLDER, filename)

    img.save(path)

    return filename


# ==============================
# GENERATE CAMPAIGN API
# ==============================

@app.route("/generate-campaign", methods=["POST"])
def generate_campaign():

    data = request.json

    business = data.get("business")
    product = data.get("product")
    offer = data.get("offer")
    festival = data.get("festival")
    location = data.get("location")

    # AI content
    ai_result = generate_marketing_content(
        business,
        product,
        offer,
        festival,
        location
    )

    # Generate poster
    poster_filename = create_poster(business, product, offer)

    poster_url = request.host_url + "poster/" + poster_filename

    return jsonify({
        "caption": ai_result.get("caption", ""),
        "hashtags": ai_result.get("hashtags", ""),
        "poster": poster_url
    })


# ==============================
# SERVE POSTER FILE
# ==============================

@app.route("/poster/<filename>")
def serve_poster(filename):
    return send_from_directory(POSTER_FOLDER, filename)

# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )