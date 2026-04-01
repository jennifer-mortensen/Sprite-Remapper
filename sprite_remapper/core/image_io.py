from PIL import Image


def load_image(path):
    return Image.open(path).convert("RGBA")


def save_image(image, path):
    image.save(path, "PNG")