from __future__ import annotations


import math


class Vector:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: Vector) -> Vector | None:
        if type(other) is Vector:
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        return None

    def __sub__(self, other: Vector) -> Vector | None:
        if type(other) is Vector:
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        return None

    def __mul__(self, other: Vector | int | float) -> Vector | float | None:
        if type(other) is int or float:
            return Vector(self.x * other, self.y * other, self.z * other)
        elif type(other) is Vector:
            return self.x * other.x + self.y * other.y + self.z * other.z
        return None

    def __truediv__(self, other: int | float) -> Vector | None:
        if type(other) is int or float:
            return Vector(self.x / other, self.y / other, self.z / other)
        return None

    def __floordiv__(self, other: int | float) -> Vector | None:
        if type(other) is int or float:
            return Vector(self.x // other, self.y // other, self.z // other)
        return None

    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> Vector:
        return Vector(self.x / self.length(), self.y / self.length(), self.z / self.length())

    @staticmethod
    def cross_product(vector1: Vector, vector2: Vector) -> Vector:
        x = vector1.y * vector2.z - vector1.z * vector2.y
        y = vector1.z * vector2.x - vector1.x * vector2.z
        z = vector1.x * vector2.y - vector1.y * vector2.x
        return Vector(x, y, z)

    def to_tuple(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'
