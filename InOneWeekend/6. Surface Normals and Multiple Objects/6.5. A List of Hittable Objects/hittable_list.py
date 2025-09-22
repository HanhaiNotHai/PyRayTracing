from hittable import HitRecord, Hittable
from ray import Ray


class HittableList(Hittable):

    def __init__(self, hittable: Hittable | None = None):
        self.hittables = [hittable] if hittable is not None else []

    def clear(self):
        self.hittables = []

    def add(self, hittable: Hittable):
        self.hittables.append(hittable)

    def hit(self, r: Ray, ray_tmin: float, ray_tmax: float, rec: HitRecord) -> bool:
        hit_anything = False

        for hittable in self.hittables:
            if hittable.hit(r, ray_tmin, rec.t if hit_anything else ray_tmax, rec):
                hit_anything = True

        return hit_anything
