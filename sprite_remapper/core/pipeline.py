from .image_io import load_image, save_image
from .tile import slice_tiles, assemble_tiles
from sprite_remapper.color.matcher import get_matcher


def run_pipeline(input_path, output_path, tile_width, tile_height, palette, color_space):
    image = load_image(input_path)

    tiles = slice_tiles(image, tile_width, tile_height)

    matcher = get_matcher(palette, color_space)

    processed_tiles = []

    for tile in tiles:
        processed_tiles.append(process_tile(tile, matcher))

    result = assemble_tiles(processed_tiles, image.size, tile_width, tile_height)

    save_image(result, output_path)


def process_tile(tile, matcher):
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