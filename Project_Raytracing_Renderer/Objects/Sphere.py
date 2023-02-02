from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Materials.Material import Material
import math


class Sphere:
    def __init__(self, origin: Vector, radius: float, material: Material) -> None:
        self.origin = origin
        self.radius = radius
        self.material = material

    def hits(self, ray: Ray, t_min: float, t_max: float) -> tuple[Vector, Vector, Material, float] | None:
        oc = ray.origin - self.origin
        a = ray.direction.length()**2
        half_b = oc * ray.direction
        c = oc.length()**2 - self.radius**2

        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return None

        sqrtd = math.sqrt(discriminant)

        root = (-half_b - sqrtd) / a

        if not t_min < root < t_max:
            root = (-half_b + sqrtd) / a
            if not t_min < root < t_max:
                return None

        intersection_point = ray.position(root)
        normal_vector = (intersection_point - self.origin) / self.radius

        return intersection_point, normal_vector, self.material, root
