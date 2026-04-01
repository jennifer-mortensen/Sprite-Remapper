from .distance import rgb_distance


class NearestColorMatcher:
    def __init__(self, palette_colors):
        self.palette = palette_colors

    def match(self, color):
        best_color = None
        best_dist = float("inf")

        for p in self.palette:
            dist = rgb_distance(color, p)

            if dist < best_dist:
                best_dist = dist
                best_color = p

        return best_color


def flatten_palette(palette):
    colors = []
    for ramp in palette["ramps"]:
        for c in ramp["colors"]:
            colors.append(tuple(c))
    return colors


def get_matcher(palette, color_space):
    colors = flatten_palette(palette)

    # v1: ignore LAB even if requested (we’ll wire it later cleanly)
    return NearestColorMatcher(colors)