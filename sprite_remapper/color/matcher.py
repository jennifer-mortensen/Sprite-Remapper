from .distance import rgb_distance, lab_distance
from .lab import rgb_to_lab


class NearestColorMatcher:
    def __init__(self, palette_colors, color_space="rgb"):
        self.color_space = color_space

        if color_space == "lab":
            self.palette = [rgb_to_lab(c) for c in palette_colors]
            self.original_palette = palette_colors
        else:
            self.palette = palette_colors

    def match(self, color):
        if self.color_space == "lab":
            color_converted = rgb_to_lab(color)
            distance_fn = lab_distance
        else:
            color_converted = color
            distance_fn = rgb_distance

        best_color = None
        best_dist = float("inf")

        for i, p in enumerate(self.palette):
            dist = distance_fn(color_converted, p)

            if dist < best_dist:
                best_dist = dist
                best_color = (
                    self.original_palette[i]
                    if self.color_space == "lab"
                    else p
                )

        return best_color


def flatten_palette(palette):
    colors = []
    for ramp in palette["ramps"]:
        for c in ramp["colors"]:
            colors.append(tuple(c))
    return colors


def get_matcher(palette, color_space):
    colors = flatten_palette(palette)
    return NearestColorMatcher(colors, color_space)