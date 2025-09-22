from vector import Vector3

Color = Vector3


def write_color(pixel_color: Color):
    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    rbyte = int(255.999 * r)
    gbyte = int(255.999 * g)
    bbyte = int(255.999 * b)

    print(f"{rbyte} {gbyte} {bbyte}")
