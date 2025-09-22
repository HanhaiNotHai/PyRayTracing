from __future__ import annotations

import math


class Vector3:

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
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


Point3 = Vector3
