import math

RGB = tuple[int, int, int]
XYZ = tuple[float, float, float]
LAB = tuple[float, float, float]

def rgb_to_xyz(r: int, g: int, b: int) -> XYZ:
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

def rgb_to_lab(rgb: RGB) -> LAB:
    x, y, z = rgb_to_xyz(*rgb)
    return xyz_to_lab(x, y, z)