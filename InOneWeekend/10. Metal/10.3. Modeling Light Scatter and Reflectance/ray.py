from vector import Point3, Vector3


class Ray:

    def __init__(self, origin: Point3, direction: Vector3):
        self.origin = origin
        self.direction = direction

    def set(self, origin: Point3, direction: Vector3):
        self.origin = origin
        self.direction = direction

    def __repr__(self) -> str:
        return f'Ray(origin = {self.origin}, direction = {self.direction})'

    def at(self, t: float) -> Point3:
        return self.origin + t * self.direction
