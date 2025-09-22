from vector import Point3, Vector3


class Ray:

    def __init__(self, origin: Point3, direction: Vector3):
        self.orig = origin
        self.dir = direction

    @property
    def origin(self) -> Point3:
        return self.orig

    @property
    def direction(self) -> Vector3:
        return self.dir

    def at(self, t: float) -> Point3:
        return self.orig + t * self.dir
