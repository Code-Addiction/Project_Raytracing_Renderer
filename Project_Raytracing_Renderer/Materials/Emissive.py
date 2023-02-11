from __future__ import annotations

from Project_Raytracing_Renderer.Materials.Material import Material
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Ray import Ray


class Emissive(Material):
    """
    Representation of emissive materials

    :param color: Color of the material
    :param intensity: Intensity of the emitted light (0 to 1)
    """
    def __init__(self, color: Vector, intensity: float):
        super().__init__(color)
        self._intensity = intensity

    def scatter(self, ray: Ray, intersection_point: Vector, normal_vector: Vector) -> tuple[Ray, Vector] | None:
        """
        Calculates how a ray is reflected

        :param ray: Ray that hits the object
        :param intersection_point: Point where the ray hits the object
        :param normal_vector: Normal vector at the point of intersection
        :return: None because no ray is reflected
        """
        return None

    def emit(self) -> Vector:
        """
        Determines emitted color

        :return: Emitted color
        """
        return self.color * self._intensity
