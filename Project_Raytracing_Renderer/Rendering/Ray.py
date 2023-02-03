from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Vector import Vector


class Ray:
    def __init__(self, origin: Vector, direction: Vector, time: float | None = None) -> None:
        self.origin = origin
        self.direction = direction
        self.time = time

    def position(self, t: float) -> Vector:
        return self.origin + self.direction * t
