from interval import Interval
from vector import Vector3

Color = Vector3


def write_color(pixel_color: Color):
    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    # Translate the [0,1] component values to the byte range [0,255].
    intensity = Interval(0, 0.999)
    rbyte = int(255.999 * intensity.clamp(r))
    gbyte = int(255.999 * intensity.clamp(g))
    bbyte = int(255.999 * intensity.clamp(b))

    # Write out the pixel color components.
    print(f"{rbyte} {gbyte} {bbyte}")
