from __future__ import annotations

import numpy as np

RNG = np.random.default_rng()


class Vector3:

    def __init__(self, x: np.ndarray | float = 0, y: float = 0, z: float = 0):
        if isinstance(x, np.ndarray):
            self.e = x
        else:
            self.e = np.array([x, y, z], dtype=np.float64)

    @property
    def x(self) -> float:
        return self.e[0]

    @x.setter
    def x(self, e: float):
        self.e[0] = e

    @property
    def y(self) -> float:
        return self.e[1]

    @y.setter
    def y(self, e: float):
        self.e[1] = e

    @property
    def z(self) -> float:
        return self.e[2]

    @z.setter
    def z(self, e: float):
        self.e[2] = e

    def set(self, x: np.ndarray | float, y: float = 0, z: float = 0):
        if isinstance(x, np.ndarray):
            self.e = x
        else:
            self.e = np.array([x, y, z], dtype=np.float64)

    def __repr__(self) -> str:
        return f'Vector3({self.x}, {self.y}, {self.z})'

    def __getitem__(self, i: int) -> float:
        return self.e[i]

    def __setitem__(self, i: int, e: float):
        self.e[i] = e

    def __neg__(self):
        return Vector3(-self.e)

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.e + other.e)

    def __iadd__(self, other: Vector3) -> Vector3:
        self.e += other.e
        return self

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(self.e - other.e)

    def __isub__(self, other: Vector3) -> Vector3:
        self.e -= other.e
        return self

    def __mul__(self, other: float | int | Vector3) -> Vector3:
        if isinstance(other, Vector3):
            return Vector3(self.e * other.e)
        return Vector3(self.e * other)

    def __rmul__(self, other: float | int) -> Vector3:
        return self * other

    def __imul__(self, other: float | int | Vector3) -> Vector3:
        if isinstance(other, Vector3):
            self.e *= other.e
            return self
        self.e *= other
        return self

    def __truediv__(self, other: float | int) -> Vector3:
        return self * (1 / other)

    def __itruediv__(self, other: float | int) -> Vector3:
        return self.__imul__(1 / other)

    def length_squared(self) -> float:
        return np.sum(self.e * self.e)

    def length(self) -> float:
        return np.linalg.norm(self.e)

    def dot(self, other: Vector3) -> float:
        return self.e.dot(other.e)

    def cross(self, other: Vector3) -> Vector3:
        return Vector3(np.cross(self.e, other.e))

    def unit_vector(self) -> Vector3:
        return self / self.length()

    @staticmethod
    def random(min_val: float | None = None, max_val: float | None = None) -> Vector3:
        if min_val is None and max_val is None:
            return Vector3(RNG.random(3))
        return Vector3(RNG.uniform(min_val, max_val, (3)))

    def near_zero(self) -> np.bool:
        '''Return True if the vector is close to zero in all dimensions.'''
        s = 1e-8
        return np.all(np.abs(self.e) < s)


def dot(u: Vector3, v: Vector3) -> float:
    return np.dot(u.e, v.e)


def cross(u: Vector3, v: Vector3) -> Vector3:
    return Vector3(np.cross(u.e, v.e))


def unit_vector(v: Vector3) -> Vector3:
    return v / v.length()


def random_in_unit_disk() -> Vector3:
    while True:
        x, y = RNG.uniform(-1, 1, (2))
        p = Vector3(x, y, 0)
        if p.length_squared() < 1:
            return p


def random_unit_vector() -> Vector3:
    while True:
        p = Vector3.random(-1, 1)
        lensq = p.length_squared()
        if 1e-160 < lensq <= 1:
            return p / np.sqrt(lensq)


def random_on_hemisphere(normal: Vector3) -> Vector3:
    on_unit_sphere = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0:  # In the same hemisphere as the normal
        return on_unit_sphere
    return -on_unit_sphere


def reflect(v: Vector3, n: Vector3) -> Vector3:
    return v - 2 * dot(v, n) * n


def refract(uv: Vector3, n: Vector3, etai_over_etat: float) -> Vector3:
    cos_theta = min(dot(-uv, n), 1)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -np.sqrt(np.abs(1 - r_out_perp.length_squared())) * n
    return r_out_perp + r_out_parallel


Point3 = Vector3
