from __future__ import annotations

import math

import cython


@cython.cclass
class Interval:

    empty: Interval
    universe: Interval

    def __init__(self, min_val: cython.double = math.inf, max_val: cython.double = -math.inf):
        self.min: cython.double = min_val
        self.max: cython.double = max_val

    def size(self) -> cython.double:
        return self.max - self.min

    def contains(self, x: cython.double) -> bool:
        return self.min <= x <= self.max

    def surrounds(self, x: cython.double) -> bool:
        return self.min < x < self.max

    @cython.cfunc
    def clamp(self, x: cython.double) -> cython.double:
        if x < self.min:
            return self.min
        if x > self.max:
            return self.max
        return x


Interval.empty = Interval(math.inf, -math.inf)
Interval.universe = Interval(-math.inf, math.inf)
