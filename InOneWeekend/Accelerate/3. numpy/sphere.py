from __future__ import annotations

import numpy as np
from numba import njit

from hittable import HitRecord, Hittable
from interval import Interval
from material import Material
from ray import Ray
from vector import Point3, _vector_dot, _vector_length_squared


@njit
def _sphere_hit_optimized(
    ray_origin: np.ndarray,
    ray_direction: np.ndarray,
    sphere_center: np.ndarray,
    radius: float,
    t_min: float,
    t_max: float,
) -> tuple[bool, float]:
    """
    Optimized sphere-ray intersection test.
    Returns (hit, t) where hit is bool and t is the intersection parameter.
    """
    oc = sphere_center - ray_origin
    a = _vector_length_squared(ray_direction)
    h = _vector_dot(ray_direction, oc)
    c = _vector_length_squared(oc) - radius * radius

    discriminant = h * h - a * c
    if discriminant < 0:
        return False, 0.0

    sqrtd = np.sqrt(discriminant)

    # Find the nearest root that lies in the acceptable range
    root = (h - sqrtd) / a
    if root <= t_min or root >= t_max:
        root = (h + sqrtd) / a
        if root <= t_min or root >= t_max:
            return False, 0.0

    return True, root


class Sphere(Hittable):

    def __init__(self, center: Point3, radius: float, mat: Material):
        self.center = center
        self.radius = max(0, radius)
        self.mat = mat

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        hit, root = _sphere_hit_optimized(
            r.origin.e, r.direction.e, self.center.e, self.radius, ray_t.min, ray_t.max
        )
        if not hit:
            return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.mat

        return True
