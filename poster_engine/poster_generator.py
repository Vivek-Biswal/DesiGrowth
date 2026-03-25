from PIL import Image, ImageDraw, ImageFont
import os
import uuid


def center_text(draw, text, font, y, width, color=(0, 0, 0)):
    text_width = draw.textlength(text, font=font)
    x = (width - text_width) / 2

    draw.text((x+2, y+2), text, fill="gray", font=font)

    draw.text((x, y), text, fill=color, font=font)


def wrap_text(text, max_chars=30):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        if len(line + word) < max_chars:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "

    lines.append(line)
    return lines


def generate_poster(business, product, offer, caption, image_path):

    output_folder = "poster_engine/generated"
    os.makedirs(output_folder, exist_ok=True)

    width = 900
    height = 900

    poster = Image.new("RGB", (width, height))
    draw_bg = ImageDraw.Draw(poster)

    for y in range(height):
        r = 255
        g = int(200 + (y / height) * 55)
        b = int(230 + (y / height) * 25)
        draw_bg.line([(0, y), (width, y)], fill=(r, g, b))

    draw = ImageDraw.Draw(poster)

    draw.rounded_rectangle(
        [(210, 150), (710, 570)],
        radius=30,
        fill=(200, 200, 200)
    )

    draw.rounded_rectangle(
        [(200, 140), (700, 560)],
        radius=30,
        fill=(255, 255, 255)
    )

    if image_path and os.path.exists(image_path):
        product_img = Image.open(image_path).convert("RGBA")
        product_img = product_img.resize((350, 350))

        shadow = Image.new("RGBA", (360, 360), (0, 0, 0, 50))
        poster.paste(shadow, (280, 180), shadow)

        poster.paste(product_img, (275, 175), product_img)

    try:
        title_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 65)
        text_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 40)
        small_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    center_text(draw, business.upper(), title_font, 50, width, color=(30, 30, 30))

    draw.line([(300, 110), (600, 110)], fill=(255, 100, 100), width=4)

    center_text(draw, product, text_font, 600, width)

    offer = "★ " + offer + " ★"

    draw.rounded_rectangle(
        [(200, 630), (700, 700)],
        radius=25,
        fill=(255, 90, 90)
    )
    center_text(draw, offer, text_font, 640, width, color=(255, 255, 255))

    caption = ">> " + caption
    lines = wrap_text(caption)

    y_text = 700
    for line in lines:
        center_text(draw, line, text_font, y_text, width, color=(50, 50, 50))
        y_text += 40

    center_text(draw, "Best Deals Near You!", text_font, 820, width, color=(80, 80, 80))

    draw.text((20, 860), "Powered by DesiGrowth", fill="gray", font=small_font)

    draw.rectangle([(10, 10), (width-10, height-10)], outline=(100, 100, 100), width=2)

    filename = f"poster_{uuid.uuid4().hex}.png"
    filepath = os.path.join(output_folder, filename)

    poster.save(filepath)

    return filepath
