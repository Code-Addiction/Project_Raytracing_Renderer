from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Ray import Ray
import math


class Material:
    def __init__(self, color: Vector) -> None:
        self.color = color

    def scatter(self, ray: Ray, intersection_point: Vector, normal_vector: Vector) -> tuple[Ray, Vector] | None:
        raise NotImplementedError

    @staticmethod
    def reflect(direction: Vector, normal_vector: Vector) -> Vector:
        return direction - normal_vector * (direction * normal_vector) * 2

    @staticmethod
    def refract(direction: Vector, normal_vector: Vector, refraction_ratio: float, factor: int) -> Vector:
        cos_theta = min(direction * normal_vector * -1 * factor, 1)
        ray_perp = (direction + normal_vector * cos_theta * factor) * refraction_ratio
        ray_parl = normal_vector * -math.sqrt(math.fabs(1 - ray_perp.length() ** 2)) * factor

        return ray_perp + ray_parl
