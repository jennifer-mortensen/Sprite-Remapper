RGB = tuple[int, int, int]
LAB = tuple[float, float, float]

def rgb_distance(c1: RGB, c2: RGB) -> float:
    return (
        (c1[0] - c2[0]) ** 2 +
        (c1[1] - c2[1]) ** 2 +
        (c1[2] - c2[2]) ** 2
    )

def lab_distance(c1: LAB, c2: LAB) -> float:
    return (
        (c1[0] - c2[0]) ** 2 +
        (c1[1] - c2[1]) ** 2 +
        (c1[2] - c2[2]) ** 2
    )