from __future__ import annotations

from Project_Raytracing_Renderer.Materials import Material
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Ray import Ray
import math
import random


class Transmissive(Material):
    """
        Representation of transmissive materials

        :param color: Color of the material
        :param refraction_index: Refraction index
        """
    def __init__(self, color: Vector, refraction_index: float):
        super().__init__(color)
        self._refraction_index = refraction_index

    def scatter(self, ray: Ray, intersection_point: Vector, normal_vector: Vector) -> tuple[Ray, Vector] | None:
        """
        Calculates how a ray is reflected/refracted

        :param ray: Ray that hits the object
        :param intersection_point: Point where the ray hits the object
        :param normal_vector: Normal vector at the point of intersection
        :return: Reflected/refracted ray and the material's color
        """
        if ray.direction * normal_vector <= 0:
            factor = 1
            refraction_ratio = 1 / self._refraction_index
        else:
            factor = -1
            refraction_ratio = self._refraction_index

        direction_normalized = ray.direction.normalize()

        cos_theta = min(direction_normalized * normal_vector * -1 * factor, 1)
        sin_theta = math.sqrt(1 - cos_theta**2)

        r0 = ((1 - refraction_ratio) / (1 + refraction_ratio))**2
        reflectance = r0 + (1 - r0) * pow(1 - cos_theta, 5)

        if refraction_ratio * sin_theta > 1 or reflectance > random.random():
            direction = Material.reflect(direction_normalized, normal_vector)
        else:
            direction = Material.refract(direction_normalized, normal_vector, refraction_ratio, factor)

        return Ray(intersection_point, direction, ray.time), self.color
