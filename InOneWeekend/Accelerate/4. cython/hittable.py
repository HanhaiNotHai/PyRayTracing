from __future__ import annotations

from abc import ABC, abstractmethod

import cython

from interval import Interval
from material import Material
from ray import Ray
from vector import Point3, Vector3, dot


@cython.cclass
class HitRecord:

    def __init__(
        self,
        p: Point3 | None = None,
        normal: Vector3 | None = None,
        mat: Material | None = None,
        t: cython.double = 0.0,
        front_face: bool = False,
    ):
        self.p = p if p is not None else Point3()
        self.normal = normal if normal is not None else Vector3()
        self.mat = mat if mat is not None else Material()
        self.t: cython.double = t
        self.front_face = front_face

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
