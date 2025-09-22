from abc import ABC, abstractmethod

from interval import Interval
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
        self.p = p if p is not None else Point3()
        self.normal = normal if normal is not None else Vector3()
        self.t = t if t is not None else 0
        self.front_face = front_face if front_face is not None else False

    def set_face_normal(self, r: Ray, outward_normal: Vector3):
        '''
        Sets the hit record normal vector.
        NOTE: the parameter `outward_normal` is assumed to have unit length.
        '''

        self.front_face = dot(r.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable(ABC):

    @abstractmethod
    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        pass
