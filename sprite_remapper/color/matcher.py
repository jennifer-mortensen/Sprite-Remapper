from typing import Any
from .distance import rgb_distance, lab_distance
from .lab import rgb_to_lab


Color = tuple[int, int, int]


class NearestColorMatcher:
    def __init__(
        self,
        palette_colors: list[Color],
        color_space: str = "rgb"
    ) -> None:
        self.color_space: str = color_space

        if color_space == "lab":
            self.palette: list[Color] = [rgb_to_lab(c) for c in palette_colors]
            self.original_palette: list[Color] = palette_colors
        else:
            self.palette = palette_colors
            self.original_palette = palette_colors  # keep consistent


    def match(self, color: Color) -> Color:
        if self.color_space == "lab":
            color_converted = rgb_to_lab(color)
            distance_fn = lab_distance
        else:
            color_converted = color
            distance_fn = rgb_distance

        best_color: Color | None = None
        best_dist: float = float("inf")

        for i, p in enumerate(self.palette):
            dist: float = distance_fn(color_converted, p)

            if dist < best_dist:
                best_dist = dist
                best_color = (
                    self.original_palette[i]
                    if self.color_space == "lab"
                    else p
                )

        # At least one color should exist, but keep type checker happy
        assert best_color is not None
        return best_color


def flatten_palette(palette: dict[str, Any]) -> list[Color]:
    colors: list[Color] = []

    for ramp in palette["ramps"]:
        for c in ramp["colors"]:
            colors.append(tuple(c))  # type: ignore[arg-type]

    return colors

def get_matcher(palette: dict[str, Any],color_space: str) -> NearestColorMatcher:
    colors = flatten_palette(palette)
    return NearestColorMatcher(colors, color_space)