"""
Tile slicing and assembly utilities for sprite_remapper.

Provides helpers for breaking an image into fixed-size tiles and
reconstructing an image from processed tiles.
"""
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def slice_tiles(image: Image.Image, tile_width: int, tile_height: int) -> list[Image.Image]:
    """
    Divide an image into tiles of the given dimensions.

    Tiles are extracted left-to-right, top-to-bottom. Edge tiles will be
    padded if the image dimensions are not evenly divisible by the tile size.

    Args:
        image: The source image to slice.
        tile_width: Width of each tile in pixels.
        tile_height: Height of each tile in pixels.

    Returns:
        A list of image tiles.
    """    
    tiles: list[Image.Image] = []

    img_width, img_height = image.size
    if img_width % tile_width != 0 or img_height % tile_height != 0:
        logger.warning(
            "Image size (%s, %s) is not evenly divisible by tile size (%s, %s). "
            "Edge tiles will be padded.",
            img_width, img_height, tile_width, tile_height
    )    

    for y in range(0, img_height, tile_height):
        for x in range(0, img_width, tile_width):
            box: tuple[int, int, int, int] = (x, y, x + tile_width, y + tile_height)
            tile = image.crop(box)
            tiles.append(tile)

    return tiles

def assemble_tiles(tiles: list[Image.Image], image_size: tuple[int, int], tile_width: int, tile_height: int) -> Image.Image:
    """
    Reconstruct an image from a list of tiles.

    Tiles are placed left-to-right, top-to-bottom to match the original
    slicing order.

    Args:
        tiles: The list of processed image tiles.
        image_size: The size of the final image as (width, height).
        tile_width: Width of each tile in pixels.
        tile_height: Height of each tile in pixels.

    Returns:
        The reconstructed image.
    """    
    result = Image.new("RGBA", image_size)

    img_width, img_height = image_size

    i = 0
    for y in range(0, img_height, tile_height):
        for x in range(0, img_width, tile_width):
            result.paste(tiles[i], (x, y))
            i += 1

    return result