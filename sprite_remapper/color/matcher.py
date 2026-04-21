"""
Color matching utilities for sprite_remapper.

Provides functionality for mapping arbitrary RGB colors to the nearest
color in a palette, supporting multiple color spaces (e.g. RGB, LAB).
Includes helpers for preparing palette data for matching.
"""
from enum import Enum
from typing import Any
from .distance import rgb_distance, lab_distance
from .lab import rgb_to_lab

# ==============================
# TYPE DEFINITIONS
# ==============================
Color = tuple[int, int, int]

class ColorSpace(str, Enum):
    RGB = "rgb"
    LAB = "lab"

# ==============================
# CLASSES
# ==============================
class NearestColorMatcher:
    """
    Find the nearest color in a palette using a chosen color space.

    Supports matching in RGB or LAB space. When using LAB, palette colors
    are preconverted to improve performance during repeated comparisons.
    """    
    def __init__(
        self,
        palette_colors: list[Color],
        color_space: str| ColorSpace
    ) -> None:
        """
        Initialize the matcher with a palette and color space.

        Args:
            palette_colors: List of RGB colors defining the palette.
            color_space: The color space to use for matching ("rgb" or "lab").
        """        
        try:
            color_space = ColorSpace(color_space.lower())           
        except ValueError:
            valid = ", ".join(cs.value for cs in ColorSpace)
            raise ValueError(f"Unsupported color space '{color_space}'. Valid: {valid}")
        
        if color_space == ColorSpace.LAB:
            self.convert = rgb_to_lab
            self.distance = lab_distance
        elif color_space == ColorSpace.RGB:
            self.convert = lambda c: c # Default color space. No conversion needed.
            self.distance = rgb_distance
        else:
            raise RuntimeError(f"Unhandled color space: {color_space}")                     

        self.palette = [self.convert(c) for c in palette_colors] # Converted palette (e.g. LAB)
        self.original_palette = palette_colors # RGB palette from JSON


    def match(self, color: Color) -> Color:
        """
        Find the nearest palette color to the given input color.

        Converts the input color to the configured color space (if needed),
        computes distances to all palette colors, and returns the closest match.

        Args:
            color: The input RGB color to match.

        Returns:
            The nearest matching RGB color from the palette.
        """        
        color_converted = self.convert(color)

        best_index = None
        best_dist = float("inf")

        for index, palette_color in enumerate(self.palette):
            dist = self.distance(color_converted, palette_color)

            if dist < best_dist:
                best_dist = dist
                best_index = index
        if best_index is None:
            raise RuntimeError("No palette match found")           

        return self.original_palette[best_index]

# ==============================
# HIGH LEVEL FUNCTIONS
# ==============================
def flatten_palette(palette: dict[str, Any]) -> list[Color]:
    """
    Extract all colors from a palette definition into a flat list.

    Args:
        palette: Palette data containing ramps of colors.

    Returns:
        A list of RGB colors as tuples.
    """    
    colors: list[Color] = []

    for ramp in palette["ramps"]:
        for c in ramp["colors"]:
            colors.append(tuple(c))  # type: ignore[arg-type]

    return colors

def get_matcher(palette: dict[str, Any], color_space: str | ColorSpace) -> NearestColorMatcher:
    """
    Create a color matcher from palette data and configuration.

    Args:
        palette: Palette data containing color ramps.
        color_space: The color space to use for matching.

    Returns:
        An initialized NearestColorMatcher instance.
    """    
    colors = flatten_palette(palette)
    return NearestColorMatcher(colors, color_space)