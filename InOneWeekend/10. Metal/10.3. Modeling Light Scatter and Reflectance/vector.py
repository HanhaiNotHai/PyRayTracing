from __future__ import annotations

import math
import random


class Vector3:

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def set(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f'Vector3({self.x}, {self.y}, {self.z})'

    def __getitem__(self, i: int) -> float:
        return [self.x, self.y, self.z][i]

    def __setitem__(self, i: int, e: float):
        if i == 0:
            self.x = e
        elif i == 1:
            self.y = e
        elif i == 2:
            self.z = e

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other: Vector3) -> Vector3:
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other: Vector3) -> Vector3:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, other: float | int | Vector3) -> Vector3:
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: float | int) -> Vector3:
        return self * other

    def __imul__(self, other: float | int | Vector3) -> Vector3:
        if isinstance(other, Vector3):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
            return self
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    def __truediv__(self, other: float | int) -> Vector3:
        return self * (1 / other)

    def __itruediv__(self, other: float | int) -> Vector3:
        return self.__imul__(1 / other)

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def dot(self, other: Vector3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3) -> Vector3:
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def unit_vector(self) -> Vector3:
        return self / self.length()

    @staticmethod
    def random(min_val: float | None = None, max_val: float | None = None) -> Vector3:
        assert min_val is None and max_val is None or min_val is not None and max_val is not None
        if isinstance(min_val, float) and isinstance(max_val, float):
            return Vector3(
                random.uniform(min_val, max_val),
                random.uniform(min_val, max_val),
                random.uniform(min_val, max_val),
            )
        return Vector3(random.random(), random.random(), random.random())

    def near_zero(self) -> bool:
        '''Return True if the vector is close to zero in all dimensions.'''
        s = 1e-8
        return abs(self.x) < s and abs(self.y) < s and abs(self.z) < s


def dot(u: Vector3, v: Vector3) -> float:
    return u.x * v.x + u.y * v.y + u.z * v.z


def cross(u: Vector3, v: Vector3) -> Vector3:
    return Vector3(
        u.y * v.z - u.z * v.y,
        u.z * v.x - u.x * v.z,
        u.x * v.y - u.y * v.x,
    )


def unit_vector(v: Vector3) -> Vector3:
    return v / v.length()


def random_unit_vector() -> Vector3:
    while True:
        p = Vector3.random(-1, 1)
        lensq = p.length_squared()
        if 1e-160 < lensq <= 1:
            return p / math.sqrt(lensq)


def random_on_hemisphere(normal: Vector3) -> Vector3:
    on_unit_sphere = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0:  # In the same hemisphere as the normal
        return on_unit_sphere
    return -on_unit_sphere


Point3 = Vector3
