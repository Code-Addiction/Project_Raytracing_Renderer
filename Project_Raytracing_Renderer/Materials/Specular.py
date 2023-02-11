from __future__ import annotations

from Project_Raytracing_Renderer.Materials.Material import Material
from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Rendering.Vector import Vector
import random


class Specular(Material):
    """
        Representation of specular materials

        :param color: Color of the material
        :param fuzz: Factor how clear the reflection should be (default: 0)
        """
    def __init__(self, color: Vector, fuzz: float = 0):
        super().__init__(color)
        self.fuzz = fuzz

    def scatter(self, ray: Ray, intersection_point: Vector,
                normal_vector: Vector) -> tuple[Ray, Vector] | None:
        """
        Calculates how a ray is reflected

        :param ray: Ray that hits the object
        :param intersection_point: Point where the ray hits the object
        :param normal_vector: Normal vector at the point of intersection
        :return: Either the reflected ray and the material's color or None if no ray is reflected
        """
        reflected = Material.reflect(ray.direction.normalize(), normal_vector)

        if self.fuzz > 0:
            fuzz_reflection = None
            while fuzz_reflection is None:
                to_test = Vector(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
                if to_test.length() ** 2 < 1:
                    fuzz_reflection = to_test

            reflected = reflected + fuzz_reflection * self.fuzz

        if reflected * normal_vector > 0:
            return Ray(intersection_point, reflected, ray.time), self.color
        return None
