from PIL import Image, ImageDraw, ImageFont
import os
import uuid


def generate_poster(business, product, offer, caption, image_path):

    # Create output folder
    output_folder = "poster_engine/generated"
    os.makedirs(output_folder, exist_ok=True)

    # Create blank poster
    width = 800
    height = 800

    poster = Image.new("RGB", (width, height), color=(240, 248, 255))

    draw = ImageDraw.Draw(poster)

    # Fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 30)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Title
    draw.text((50, 100), business, fill="black", font=title_font)

    # Product
    draw.text((50, 250), f"Product: {product}", fill="black", font=text_font)

    # Offer
    draw.text((50, 350), f"Offer: {offer}", fill="red", font=text_font)

    # Caption
    draw.text((50, 500), caption[:100], fill="black", font=text_font)

    # Unique filename
    filename = f"poster_{uuid.uuid4().hex}.png"

    filepath = os.path.join(output_folder, filename)

    poster.save(filepath)

    return filepath
if __name__ == "__main__":

    path = generate_poster(
        "Sharma Grocery",
        "Premium Rice",
        "20% OFF",
        "Celebrate Diwali with amazing savings!",
        ""
    )

    print("Poster created at:", path)
