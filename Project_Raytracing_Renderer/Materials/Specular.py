from __future__ import annotations

from Project_Raytracing_Renderer.Materials.Material import Material
from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Rendering.Vector import Vector
import random


class Specular(Material):
    def __init__(self, color: Vector, fuzz: float = 0):
        super().__init__(color)
        self.fuzz = fuzz

    def scatter(self, ray: Ray, intersection_point: Vector,
                normal_vector: Vector) -> tuple[Ray, Vector] | None:
        reflected = Material.reflect(ray.direction.normalize(), normal_vector)

        if self.fuzz > 0:
            fuzz_reflection = None
            while fuzz_reflection is None:
                to_test = Vector(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
                if to_test.length() ** 2 < 1:
                    fuzz_reflection = to_test

            reflected = reflected + fuzz_reflection * self.fuzz

        if reflected * normal_vector > 0:
            return Ray(intersection_point, reflected), self.color
        return None
