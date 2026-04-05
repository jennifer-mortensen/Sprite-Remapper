from pathlib import Path
from PIL import Image

def load_image(path: str | Path) -> Image.Image:
    return Image.open(path).convert("RGBA")

def save_image(image: Image.Image, path: str | Path) -> None:
    image.save(path, "PNG")