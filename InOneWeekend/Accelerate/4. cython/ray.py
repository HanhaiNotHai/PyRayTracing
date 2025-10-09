from __future__ import annotations

from vector import Point3, Vector3


class Ray:

    def __init__(self, origin: Point3 | None = None, direction: Vector3 | None = None):
        self.origin = origin if origin is not None else Point3()
        self.direction = direction if direction is not None else Vector3()

    def set(self, origin: Point3, direction: Vector3):
        self.origin = origin
        self.direction = direction

    def __repr__(self) -> str:
        return f'Ray(origin = {self.origin}, direction = {self.direction})'

    def at(self, t: float) -> Point3:
        return self.origin + t * self.direction
