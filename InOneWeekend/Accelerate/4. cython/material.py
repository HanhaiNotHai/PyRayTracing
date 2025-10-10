from __future__ import annotations

import random
from typing import TYPE_CHECKING

import cython
from cython.cimports.libc.math import sqrt

from color import Color
from ray import Ray
from vector import dot, random_unit_vector, reflect, refract, unit_vector

if TYPE_CHECKING:
    from hittable import HitRecord


class Material:

    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> cython.bint:
        return False


class Lambertian(Material):

    def __init__(self, albedo: Color):
        self.albedo = albedo

    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> cython.bint:
        scatter_direction = rec.normal + random_unit_vector()

        # Catch degenerate scatter direction
        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered.set(rec.p, scatter_direction)
        attenuation.set(self.albedo.x, self.albedo.y, self.albedo.z)
        return True


class Metal(Material):

    def __init__(self, albedo: Color, fuzz: cython.double):
        self.albedo = albedo
        self.fuzz: cython.double = fuzz if fuzz < 1 else 1

    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> cython.bint:
        reflected = reflect(r_in.direction, rec.normal)
        reflected = unit_vector(reflected) + (self.fuzz * random_unit_vector())
        scattered.set(rec.p, reflected)
        attenuation.set(self.albedo.x, self.albedo.y, self.albedo.z)
        return dot(scattered.direction, rec.normal) > 0


class Dielectric(Material):

    def __init__(self, refraction_index: cython.double):
        # Refractive index in vacuum or air, or the ratio of the material's refractive index over
        # the refractive index of the enclosing media
        self.refraction_index: cython.double = refraction_index

    @staticmethod
    def reflectance(cosine: cython.double, refraction_index: cython.double) -> cython.double:
        '''Use Schlick's approximation for reflectance.'''
        r0: cython.double = (1.0 - refraction_index) / (1 + refraction_index)
        r0 = r0 * r0
        return r0 + (1.0 - r0) * (1.0 - cosine) ** 5

    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> cython.bint:
        attenuation.set(1.0, 1.0, 1.0)
        ri: cython.double = (
            1.0 / self.refraction_index if rec.front_face else self.refraction_index
        )

        unit_direction = unit_vector(r_in.direction)
        cos_theta: cython.double = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta: cython.double = sqrt(1.0 - cos_theta * cos_theta)

        cannot_refract: cython.bint = ri * sin_theta > 1.0

        if cannot_refract or self.reflectance(cos_theta, ri) > random.random():
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, ri)

        scattered.set(rec.p, direction)
        return True
