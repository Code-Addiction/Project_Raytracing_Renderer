from Project_Raytracing_Renderer.Vector import Vector


class Ray:
    def __init__(self, origin: Vector, direction: Vector) -> None:
        self._origin = origin
        self._direction = direction

    def position(self, t: float) -> Vector:
        return self._origin + self._direction * t

    def color(self) -> Vector:
        unit_direction = self._direction.normalize()
        t = 0.5 * (unit_direction.y + 1)
        return Vector(255, 255, 255) * (1 - t) + Vector(0.5 * 255, 0.7 * 255, 255) * t
