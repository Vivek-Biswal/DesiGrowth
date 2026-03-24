from PIL import Image, ImageDraw, ImageFont
import os
import uuid


def generate_poster(business, product, offer, caption):
    folder = "poster_engine/generated"
    os.makedirs(folder, exist_ok=True)

    img = Image.new("RGB", (900, 900), (255, 245, 230))
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()

    draw.text((50, 100), business, fill="black", font=font)
    draw.text((50, 250), f"Product: {product}", fill="black", font=font)
    draw.text((50, 350), f"Offer: {offer}", fill="red", font=font)
    draw.text((50, 500), caption[:100], fill="black", font=font)

    filename = f"poster_{uuid.uuid4().hex}.png"
    path = os.path.join(folder, filename)

    img.save(path)

    return path