from PIL import Image, ImageDraw, ImageFont
import os
import uuid


def generate_poster(business, product, offer, caption, image_path):

    output_folder = "poster_engine/generated"
    os.makedirs(output_folder, exist_ok=True)

    width = 900
    height = 900

    poster = Image.new("RGB", (width, height), color=(255, 245, 230))

    draw = ImageDraw.Draw(poster)

    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        text_font = ImageFont.truetype("arial.ttf", 40)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    draw.text((80, 120), business, fill="black", font=title_font)

    draw.text((80, 320), f"Product: {product}", fill="black", font=text_font)

    draw.text((80, 420), f"Offer: {offer}", fill="red", font=text_font)

    draw.text((80, 580), caption[:120], fill="black", font=text_font)

    filename = f"poster_{uuid.uuid4().hex}.png"

    filepath = os.path.join(output_folder, filename)

    poster.save(filepath)

    return filepath