import random

def get_product_image(product):
    product = product.lower()

    images = {
        "laptop": "XYZ_laptop.jpeg",
        "smartphone": "XYZ_smartphone.jpeg",
        "phone": "XYZ_smartphone.jpeg",
        "speaker": "speaker.jpeg",

        "butter": "amul_butter.jpeg",
        "bread": "bread.jpeg",
        "vegetable": "fruits and vegetables.jpeg",
        "fruit": "fruits and vegetables.jpeg",

        "hair oil": "hairoil.jpeg",
        "oil": "soyabean oil.jpeg",

        "onion": "onion.jpeg",
        "semolina": "semolina.jpeg"
    }

    for key in images:
        if key in product:
            return images[key]

    # If nothing matches pick random image
    return None