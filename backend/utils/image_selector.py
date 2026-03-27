import random

def get_product_image(product):
    product = product.lower()

    base_path = os.path.join("backend", "assets")

    if "vegetable" in product or "grocery" in product:
        folder = os.path.join(base_path, "vegetables")

    elif "shoe" in product:
        folder = os.path.join(base_path, "shoes")

    elif "electronic" in product:
        folder = os.path.join(base_path, "electronics")

    else:
        folder = os.path.join(base_path, "default")

    if os.path.exists(folder):
        images = os.listdir(folder)
        if images:
            return os.path.join(folder, random.choice(images))

    return None

