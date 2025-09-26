from hittable import HitRecord, Hittable
from interval import Interval
from ray import Ray


class HittableList(Hittable):

    def __init__(self, hittable: Hittable | None = None):
        self.hittables = [hittable] if hittable is not None else []

    def clear(self):
        self.hittables = []

    def add(self, hittable: Hittable):
        self.hittables.append(hittable)

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        hit_anything = False

        for hittable in self.hittables:
            if hittable.hit(r, Interval(ray_t.min, rec.t if hit_anything else ray_t.max), rec):
                hit_anything = True

        return hit_anything
