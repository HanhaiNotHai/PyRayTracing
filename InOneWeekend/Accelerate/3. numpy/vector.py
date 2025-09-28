from __future__ import annotations

import numpy as np
from numba import njit

RNG = np.random.default_rng()


# Numba optimized functions for vector operations
@njit
def _vector_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Optimized vector addition"""
    return a + b


@njit
def _vector_sub(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Optimized vector subtraction"""
    return a - b


@njit
def _vector_mul_scalar(a: np.ndarray, scalar: float) -> np.ndarray:
    """Optimized vector-scalar multiplication"""
    return a * scalar


@njit
def _vector_mul_vector(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Optimized element-wise vector multiplication"""
    return a * b


@njit
def _vector_length_squared(a: np.ndarray) -> float:
    """Optimized vector length squared calculation"""
    return a[0] * a[0] + a[1] * a[1] + a[2] * a[2]


@njit
def _vector_length(a: np.ndarray) -> float:
    """Optimized vector length calculation"""
    return np.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


@njit
def _vector_dot(a: np.ndarray, b: np.ndarray) -> float:
    """Optimized dot product"""
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


@njit
def _vector_cross(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Optimized cross product"""
    result = np.empty(3, dtype=np.float64)
    result[0] = a[1] * b[2] - a[2] * b[1]
    result[1] = a[2] * b[0] - a[0] * b[2]
    result[2] = a[0] * b[1] - a[1] * b[0]
    return result


@njit
def _vector_near_zero(a: np.ndarray) -> bool:
    """Optimized check if vector is near zero"""
    s = 1e-8
    return abs(a[0]) < s and abs(a[1]) < s and abs(a[2]) < s


@njit
def _reflect(v: np.ndarray, n: np.ndarray) -> np.ndarray:
    """Optimized reflection calculation"""
    return v - 2 * _vector_dot(v, n) * n


@njit
def _refract(uv: np.ndarray, n: np.ndarray, etai_over_etat: float) -> np.ndarray:
    """Optimized refraction calculation"""
    cos_theta = min(_vector_dot(-uv, n), 1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -np.sqrt(abs(1.0 - _vector_length_squared(r_out_perp))) * n
    return r_out_perp + r_out_parallel


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
        return Vector3(_vector_add(self.e, other.e))

    def __iadd__(self, other: Vector3) -> Vector3:
        self.e = _vector_add(self.e, other.e)
        return self

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(_vector_sub(self.e, other.e))

    def __isub__(self, other: Vector3) -> Vector3:
        self.e = _vector_sub(self.e, other.e)
        return self

    def __mul__(self, other: float | int | Vector3) -> Vector3:
        if isinstance(other, Vector3):
            return Vector3(_vector_mul_vector(self.e, other.e))
        return Vector3(_vector_mul_scalar(self.e, float(other)))

    def __rmul__(self, other: float | int) -> Vector3:
        return self * other

    def __imul__(self, other: float | int | Vector3) -> Vector3:
        if isinstance(other, Vector3):
            self.e = _vector_mul_vector(self.e, other.e)
            return self
        self.e = _vector_mul_scalar(self.e, float(other))
        return self

    def __truediv__(self, other: float | int) -> Vector3:
        return self * (1 / other)

    def __itruediv__(self, other: float | int) -> Vector3:
        return self.__imul__(1 / other)

    def length_squared(self) -> float:
        return _vector_length_squared(self.e)

    def length(self) -> float:
        return _vector_length(self.e)

    def dot(self, other: Vector3) -> float:
        return _vector_dot(self.e, other.e)

    def cross(self, other: Vector3) -> Vector3:
        return Vector3(_vector_cross(self.e, other.e))

    def unit_vector(self) -> Vector3:
        return self / self.length()

    @staticmethod
    def random(min_val: float | None = None, max_val: float | None = None) -> Vector3:
        if min_val is None and max_val is None:
            return Vector3(RNG.random(3))
        return Vector3(RNG.uniform(min_val, max_val, (3)))

    def near_zero(self) -> bool:
        '''Return True if the vector is close to zero in all dimensions.'''
        return _vector_near_zero(self.e)


def dot(u: Vector3, v: Vector3) -> float:
    return _vector_dot(u.e, v.e)


def cross(u: Vector3, v: Vector3) -> Vector3:
    return Vector3(_vector_cross(u.e, v.e))


def unit_vector(v: Vector3) -> Vector3:
    return v / v.length()


@njit
def _random_in_unit_disk_optimized() -> tuple[float, float]:
    """Optimized random point in unit disk"""
    while True:
        x = np.random.uniform(-1.0, 1.0)
        y = np.random.uniform(-1.0, 1.0)
        if x * x + y * y < 1.0:
            return x, y


@njit
def _random_unit_vector_optimized() -> np.ndarray:
    """Optimized random unit vector"""
    while True:
        x = np.random.uniform(-1.0, 1.0)
        y = np.random.uniform(-1.0, 1.0)
        z = np.random.uniform(-1.0, 1.0)
        lensq = x * x + y * y + z * z
        if 1e-160 < lensq <= 1.0:
            inv_sqrt = 1.0 / np.sqrt(lensq)
            return np.array([x * inv_sqrt, y * inv_sqrt, z * inv_sqrt], dtype=np.float64)


def random_in_unit_disk() -> Vector3:
    x, y = _random_in_unit_disk_optimized()
    return Vector3(x, y, 0)


def random_unit_vector() -> Vector3:
    return Vector3(_random_unit_vector_optimized())


def random_on_hemisphere(normal: Vector3) -> Vector3:
    on_unit_sphere = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0:  # In the same hemisphere as the normal
        return on_unit_sphere
    return -on_unit_sphere


def reflect(v: Vector3, n: Vector3) -> Vector3:
    return Vector3(_reflect(v.e, n.e))


def refract(uv: Vector3, n: Vector3, etai_over_etat: float) -> Vector3:
    return Vector3(_refract(uv.e, n.e, etai_over_etat))


Point3 = Vector3
