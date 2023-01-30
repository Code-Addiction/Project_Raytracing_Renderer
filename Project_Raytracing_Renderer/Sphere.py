from __future__ import annotations

from Project_Raytracing_Renderer.Vector import Vector
from Project_Raytracing_Renderer.Ray import Ray
from Project_Raytracing_Renderer.Material import Material
import math


class Sphere:
    def __init__(self, origin: Vector, radius: float, material: Material) -> None:
        self.origin = origin
        self.radius = radius
        self.material = material

    def hits(self, ray: Ray) -> tuple[Vector, Vector, Material, float] | None:
        oc = ray.origin - self.origin
        a = ray.direction * ray.direction
        b = 2.0 * (oc * ray.direction)
        c = (oc * oc) - self.radius**2
        if b * b - 4 * a * c >= 0:
            t_root = math.sqrt(((b / a) / 2)**2 - (c / a))
            t_basis = -((b / a) / 2)
            t1 = t_basis + t_root
            t2 = t_basis - t_root
            t = None
            if t1 >= 0 and t2 >= 0:
                t = t1 if t1 < t2 else t2
            elif t1 >= 0:
                t = t1
            elif t2 >= 0:
                t = t2
            if t is not None:
                intersection_point = ray.position(t)
                normal_vector = (intersection_point - self.origin).normalize()
                return intersection_point, normal_vector, self.material, t
        return None
