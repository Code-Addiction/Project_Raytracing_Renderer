from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Materials.Material import Material
import random


class Diffuse(Material):
    def scatter(self, ray: Ray, intersection_point: Vector, normal_vector: Vector) -> tuple[Vector, Vector]:
        reflection = None
        while reflection is None:
            to_test = Vector(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
            if to_test.length()**2 < 1:
                reflection = to_test

        return normal_vector + reflection, self.color
