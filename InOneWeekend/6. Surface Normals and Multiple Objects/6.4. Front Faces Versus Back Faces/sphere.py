import math

from hittable import HitRecord, Hittable
from ray import Ray
from vector import Point3, dot


class Sphere(Hittable):

    def __init__(self, center: Point3, radius: float):
        self.center = center
        self.radius = max(0, radius)

    def hit(self, r: Ray, ray_tmin: float, ray_tmax: float, rec: HitRecord) -> bool:
        oc = self.center - r.origin
        a = r.direction.length_squared()
        h = dot(r.direction, oc)
        c = oc.length_squared() - self.radius * self.radius

        discriminant = h * h - a * c
        if discriminant < 0:
            return False

        sqrtd = math.sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        root = (h - sqrtd) / a
        if not ray_tmin < root < ray_tmax:
            root = (h + sqrtd) / a
            if not ray_tmin < root < ray_tmax:
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)

        return True
