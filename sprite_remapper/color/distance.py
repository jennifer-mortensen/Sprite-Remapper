"""
Color distance helpers for comparing colors in different color spaces.

Provides squared-distance calculations for RGB and LAB values used
during nearest-color palette matching.
"""

# ==============================
# TYPE ALIASES
# ==============================
LAB = tuple[float, float, float]
RGB = tuple[int, int, int]

# ==============================
# DISTANCE FUNCTIONS
# ==============================
def lab_distance(c1: LAB, c2: LAB) -> float:
    """
    Return the squared Euclidean distance between two LAB colors.

    Args:
        c1: The first LAB color.
        c2: The second LAB color.

    Returns:
        The squared component distance between the two colors.
    """
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)

def rgb_distance(c1: RGB, c2: RGB) -> float:
    """
    Return the squared Euclidean distance between two RGB colors.

    Args:
        c1: The first RGB color.
        c2: The second RGB color.

    Returns:
        The squared channel distance between the two colors.
    """    
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)