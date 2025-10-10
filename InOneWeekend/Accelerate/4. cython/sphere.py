from __future__ import annotations

import cython
from cython.cimports.libc.math import sqrt

from hittable import HitRecord, Hittable
from interval import Interval
from material import Material
from ray import Ray
from vector import Point3, dot


class Sphere(Hittable):

    def __init__(self, center: Point3, radius: cython.double, mat: Material):
        self.center = center
        self.radius: cython.double = max(0., radius)
        self.mat = mat

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> cython.bint:
        oc = self.center - r.origin
        a: cython.double = r.direction.length_squared()
        h: cython.double = dot(r.direction, oc)
        c: cython.double = oc.length_squared() - self.radius * self.radius

        discriminant: cython.double = h * h - a * c
        if discriminant < 0.:
            return False

        sqrtd: cython.double = sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        root: cython.double = (h - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root):
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.mat

        return True
