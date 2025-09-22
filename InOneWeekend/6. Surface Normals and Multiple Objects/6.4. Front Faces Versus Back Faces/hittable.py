from abc import ABC, abstractmethod

from ray import Ray
from vector import Point3, Vector3, dot


class HitRecord:

    def __init__(
        self,
        p: Point3 | None = None,
        normal: Vector3 | None = None,
        t: float | None = None,
        front_face: bool | None = None,
    ):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face

    def set_face_normal(self, r: Ray, outward_normal: Vector3):
        # Sets the hit record normal vector.
        # NOTE: the parameter `outward_normal` is assumed to have unit length.

        self.front_face = dot(r.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable(ABC):

    @abstractmethod
    def hit(self, r: Ray, ray_tmin: float, ray_tmax: float, rec: HitRecord) -> bool:
        pass
