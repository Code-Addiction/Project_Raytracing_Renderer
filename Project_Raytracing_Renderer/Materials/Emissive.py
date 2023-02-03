from __future__ import annotations

from Project_Raytracing_Renderer.Materials.Material import Material
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Ray import Ray


class Emissive(Material):
    def __init__(self, color: Vector, intensity: float):
        super().__init__(color)
        self._intensity = intensity

    def scatter(self, ray: Ray, intersection_point: Vector, normal_vector: Vector) -> tuple[Ray, Vector] | None:
        return None

    def emit(self):
        return self.color * self._intensity
