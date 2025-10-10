from __future__ import annotations

import io

import cython
from cython.cimports.libc.math import sqrt

from interval import Interval
from vector import Vector3

Color = Vector3


@cython.cfunc
def linear_to_gamma(linear_component: cython.double) -> cython.double:
    if linear_component > 0:
        return sqrt(linear_component)
    return 0


def write_color(pixel_color: Color, f: io.TextIOWrapper):
    r: cython.double = pixel_color.x
    g: cython.double = pixel_color.y
    b: cython.double = pixel_color.z

    # Apply a linear to gamma transform for gamma 2
    r = linear_to_gamma(r)
    g = linear_to_gamma(g)
    b = linear_to_gamma(b)

    # Translate the [0,1] component values to the byte range [0,255].
    intensity = Interval(0, 0.999)
    rbyte: cython.int = int(255.999 * intensity.clamp(r))
    gbyte: cython.int = int(255.999 * intensity.clamp(g))
    bbyte: cython.int = int(255.999 * intensity.clamp(b))

    # Write out the pixel color components.
    f.write(f'{rbyte} {gbyte} {bbyte}\n')
