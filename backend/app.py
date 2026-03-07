from PIL import Image, ImageDraw, ImageFont
import uuid
import os

def create_poster(business, product, offer):

    width = 800
    height = 800

    # Gradient style background
    img = Image.new("RGB", (width, height), (25, 118, 210))
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 70)
        product_font = ImageFont.truetype("arial.ttf", 50)
        offer_font = ImageFont.truetype("arial.ttf", 90)
    except:
        title_font = ImageFont.load_default()
        product_font = ImageFont.load_default()
        offer_font = ImageFont.load_default()

    # Business Name
    draw.text(
        (width/2, 120),
        business,
        fill="white",
        font=title_font,
        anchor="mm"
    )

    # Product
    draw.text(
        (width/2, 350),
        product,
        fill="white",
        font=product_font,
        anchor="mm"
    )

    # Offer Highlight Box
    box_x1 = 150
    box_y1 = 450
    box_x2 = 650
    box_y2 = 600

    draw.rectangle(
        [box_x1, box_y1, box_x2, box_y2],
        fill=(255, 87, 34)
    )

    draw.text(
        (width/2, 525),
        offer,
        fill="white",
        font=offer_font,
        anchor="mm"
    )

    # Save poster
    filename = f"poster_{uuid.uuid4().hex}.png"
    path = os.path.join(POSTER_FOLDER, filename)

    img.save(path)

    return filename