from __future__ import annotations

from typing import TYPE_CHECKING

from color import Color
from ray import Ray
from vector import dot, random_unit_vector, reflect, unit_vector

if TYPE_CHECKING:
    from hittable import HitRecord


class Material:

    def scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool:
        return False


class Lambertian(Material):

    def __init__(self, albedo: Color):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool:
        scatter_direction = rec.normal + random_unit_vector()

        # Catch degenerate scatter direction
        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered.set(rec.p, scatter_direction)
        attenuation.set(self.albedo.x, self.albedo.y, self.albedo.z)
        return True


class Metal(Material):

    def __init__(self, albedo: Color, fuzz: float):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1

    def scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool:
        reflected = reflect(r_in.direction, rec.normal)
        reflected = unit_vector(reflected) + (self.fuzz * random_unit_vector())
        scattered.set(rec.p, reflected)
        attenuation.set(self.albedo.x, self.albedo.y, self.albedo.z)
        return dot(scattered.direction, rec.normal) > 0
