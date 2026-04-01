from PIL import Image


def slice_tiles(image, tile_width, tile_height):
    tiles = []

    img_width, img_height = image.size

    for y in range(0, img_height, tile_height):
        for x in range(0, img_width, tile_width):
            box = (x, y, x + tile_width, y + tile_height)
            tile = image.crop(box)
            tiles.append(tile)

    return tiles


def assemble_tiles(tiles, image_size, tile_width, tile_height):
    result = Image.new("RGBA", image_size)

    img_width, img_height = image_size

    i = 0
    for y in range(0, img_height, tile_height):
        for x in range(0, img_width, tile_width):
            result.paste(tiles[i], (x, y))
            i += 1

    return result