from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Vector import Vector


class Ray:
    """
    Defines a ray

    :param origin: Origin of the ray
    :param direction: Direction of the ray
    :param time: Point in time of the ray or None (default: None)
    """
    def __init__(self, origin: Vector, direction: Vector, time: float | None = None):
        self.origin = origin
        self.direction = direction
        self.time = time

    def position(self, t: float) -> Vector:
        """
        Computes position of ray

        :param t: Number how many times the ray has traveled its direction
        :return: Position at t
        """
        return self.origin + self.direction * t
