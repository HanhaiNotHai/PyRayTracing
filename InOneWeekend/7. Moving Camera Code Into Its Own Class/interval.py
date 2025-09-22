from __future__ import annotations

import math


class Interval:

    empty: Interval
    universe: Interval

    def __init__(self, min_val: float = math.inf, max_val: float = -math.inf):
        self.min = min_val
        self.max = max_val

    def size(self) -> float:
        return self.max - self.min

    def contains(self, x: float) -> bool:
        return self.min <= x <= self.max

    def surrounds(self, x: float) -> bool:
        return self.min < x < self.max


Interval.empty = Interval(math.inf, -math.inf)
Interval.universe = Interval(-math.inf, math.inf)
