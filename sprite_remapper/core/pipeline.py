from pathlib import Path
from typing import Any, Protocol
from PIL import Image
from .image_io import load_image, save_image
from .tile import slice_tiles, assemble_tiles
from sprite_remapper.color.matcher import get_matcher


class ColorMatcher(Protocol):
    def match(self, color: tuple[int, int, int]) -> tuple[int, int, int]: ...


def run_pipeline(input_path: str | Path, output_path: str | Path, tile_width: int, tile_height: int, palette: dict[str, Any], color_space: str) -> None:
    image: Image.Image = load_image(input_path)

    tiles: list[Image.Image] = slice_tiles(image, tile_width, tile_height)

    matcher: ColorMatcher = get_matcher(palette, color_space)

    processed_tiles: list[Image.Image] = []

    for tile in tiles:
        processed_tiles.append(process_tile(tile, matcher))

    result: Image.Image = assemble_tiles(
        processed_tiles,
        image.size,
        tile_width,
        tile_height
    )

    save_image(result, output_path)


def process_tile(tile: Image.Image, matcher: ColorMatcher) -> Image.Image:
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