"""
Color space conversion helpers for sprite_remapper.

Provides utilities for converting RGB colors into CIE XYZ and CIE LAB
representations for perceptual color-distance matching.
"""
# ==============================
# TYPE ALIASES
# ==============================
RGB = tuple[int, int, int]
XYZ = tuple[float, float, float]
LAB = tuple[float, float, float]

# ==============================
# COLOR CONVERSION FUNCTIONS
# ==============================
def rgb_to_lab(rgb: RGB) -> LAB:
    """
    Convert an RGB color value directly to CIE LAB.

    Internally converts RGB to XYZ first, then XYZ to LAB.

    Args:
        rgb: The RGB color as a three-channel tuple.

    Returns:
        The converted LAB color as a tuple of floats.
    """    
    x, y, z = rgb_to_xyz(*rgb)
    return xyz_to_lab(x, y, z)

def rgb_to_xyz(r: int, g: int, b: int) -> XYZ:
    """
    Convert an RGB color value to CIE XYZ.

    Args:
        r: Red channel value (0-255).
        g: Green channel value (0-255).
        b: Blue channel value (0-255).

    Returns:
        The converted XYZ color as a tuple of floats.
    """    
    r = r / 255
    g = g / 255
    b = b / 255

    def pivot(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r = pivot(r)
    g = pivot(g)
    b = pivot(b)

    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505

    return x, y, z

def xyz_to_lab(x: float, y: float, z: float) -> LAB:
    """
    Convert a CIE XYZ color value to CIE LAB.

    Args:
        x: X component of the XYZ color.
        y: Y component of the XYZ color.
        z: Z component of the XYZ color.

    Returns:
        The converted LAB color as a tuple of floats.
    """    
    # D65 reference white
    xr = x / 0.95047
    yr = y / 1.00000
    zr = z / 1.08883

    def pivot(c: float) -> float:
        return c ** (1 / 3) if c > 0.008856 else (7.787 * c) + (16 / 116)

    fx = pivot(xr)
    fy = pivot(yr)
    fz = pivot(zr)

    l = (116 * fy) - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)

    return l, a, b