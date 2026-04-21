"""
Core image processing pipeline for sprite_remapper.

Coordinates the full remapping workflow: loading an image, slicing it
into tiles, applying palette-based color matching, and assembling the
final output image.
"""
from pathlib import Path
from typing import Any, Protocol
from PIL import Image
from .image_io import load_image, save_image
from .tile import slice_tiles, assemble_tiles
from sprite_remapper.color.matcher import get_matcher
import logging

logger = logging.getLogger(__name__)

# ==============================
# INTERFACES
# ==============================
class ColorMatcher(Protocol):
    def match(self, color: tuple[int, int, int]) -> tuple[int, int, int]: ...

# ==============================
# HIGH LEVEL FUNCTIONS
# ==============================
def run_pipeline(input_path: str | Path, output_path: str | Path, tile_width: int, tile_height: int, palette: dict[str, Any], color_space: str) -> None:
    """
    Execute the sprite remapping pipeline.

    Loads the input image, splits it into tiles, remaps each tile's colors
    using the provided palette and color space, then reassembles and saves
    the final image.

    Args:
        input_path: Path to the source image.
        output_path: Path to write the processed image.
        tile_width: Width of each tile in pixels.
        tile_height: Height of each tile in pixels.
        palette: Palette definition used for color matching.
        color_space: Color space used for distance calculations.
    """    
    image: Image.Image = load_image(input_path)
    tiles: list[Image.Image] = slice_tiles(image, tile_width, tile_height)
    matcher: ColorMatcher = get_matcher(palette, color_space)
    processed_tiles: list[Image.Image] = []

    i = 0
    for tile in tiles:
        i+= 1
        logger.info(f"Processing tile {i}/{len(tiles)}")
        processed_tiles.append(process_tile(tile, matcher))

    result: Image.Image = assemble_tiles(
        processed_tiles,
        image.size,
        tile_width,
        tile_height
    )

    save_image(result, output_path)

def process_tile(tile: Image.Image, matcher: ColorMatcher) -> Image.Image:
    """
    Apply palette-based color remapping to a single tile.

    Iterates over each pixel, replacing its color with the nearest match
    from the palette while preserving alpha transparency.

    Args:
        tile: The image tile to process.
        matcher: Color matcher used to find nearest palette colors.

    Returns:
        The processed tile image.
    """    
    pixels = tile.load()
    width, height = tile.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]

            if a == 0:
                continue

            new_color = matcher.match((r, g, b))
            pixels[x, y] = (*new_color, a)

    return tile