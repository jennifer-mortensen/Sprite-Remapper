"""
Image loading and saving helpers for sprite_remapper.

Provides standardized file I/O wrappers for opening source images
and writing processed output images with the expected formats.
"""
from pathlib import Path
from PIL import Image

# ==============================
# I/O CONSTANTS
# ==============================
IMAGE_MODE_DEFAULT = "RGBA"
IMAGE_FORMAT_DEFAULT = "PNG"

# ==============================
# I/O FUNCTIONS
# ==============================
def load_image(path: str | Path) -> Image.Image:
    """
    Load an image file and convert it to the default working mode.

    Args:
        path: The path to the image file.

    Returns:
        The loaded image as a Pillow Image object.
    """    
    return Image.open(path).convert(IMAGE_MODE_DEFAULT)

def save_image(image: Image.Image, path: str | Path) -> None:
    """
    Save an image to disk using the default output format.

    Args:
        image: The Pillow Image to save.
        path: The destination file path.
    """    
    image.save(path, IMAGE_FORMAT_DEFAULT)