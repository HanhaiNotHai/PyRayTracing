from __future__ import annotations

import numpy as np


class Interval:

    empty: Interval
    universe: Interval

    def __init__(self, min_val: float = np.inf, max_val: float = -np.inf):
        self.min = min_val
        self.max = max_val

    def size(self) -> float:
        return self.max - self.min

    def contains(self, x: float) -> bool:
        return self.min <= x <= self.max

    def surrounds(self, x: float) -> bool:
        return self.min < x < self.max

    def clamp(self, x: float) -> float:
        return np.clip(x, self.min, self.max)


Interval.empty = Interval(np.inf, -np.inf)
Interval.universe = Interval(-np.inf, np.inf)
