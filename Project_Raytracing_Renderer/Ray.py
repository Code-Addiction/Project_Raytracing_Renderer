from __future__ import annotations

from Project_Raytracing_Renderer.Vector import Vector


class Ray:
    def __init__(self, origin: Vector, direction: Vector) -> None:
        self.origin = origin
        self.direction = direction

    def position(self, t: float) -> Vector:
        return self.origin + self.direction * t
