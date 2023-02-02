from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Ray import Ray


class Material:
    def __init__(self, color: Vector) -> None:
        self.color = color

    def scatter(self, ray: Ray, intersection_point: Vector, normal_vector: Vector) -> tuple[Ray, Vector] | None:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{type(self)} with color {self.color}"
