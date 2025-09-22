from abc import ABC, abstractmethod

from ray import Ray
from vector import Point3, Vector3


class HitRecord:

    def __init__(
        self, p: Point3 | None = None, normal: Vector3 | None = None, t: float | None = None
    ):
        self.p = p
        self.normal = normal
        self.t = t


class Hittable(ABC):

    @abstractmethod
    def hit(self, r: Ray, ray_tmin: float, ray_tmax: float, rec: HitRecord) -> bool:
        pass
