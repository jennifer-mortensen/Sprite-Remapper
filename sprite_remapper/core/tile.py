from PIL import Image

def slice_tiles(image: Image.Image, tile_width: int, tile_height: int) -> list[Image.Image]:
    tiles: list[Image.Image] = []

    img_width, img_height = image.size

    for y in range(0, img_height, tile_height):
        for x in range(0, img_width, tile_width):
            box: tuple[int, int, int, int] = (x, y, x + tile_width, y + tile_height)
            tile = image.crop(box)
            tiles.append(tile)

    return tiles

def assemble_tiles(tiles: list[Image.Image], image_size: tuple[int, int], tile_width: int, tile_height: int) -> Image.Image:
    result = Image.new("RGBA", image_size)

    img_width, img_height = image_size

    i = 0
    for y in range(0, img_height, tile_height):
        for x in range(0, img_width, tile_width):
            result.paste(tiles[i], (x, y))
            i += 1

    return result