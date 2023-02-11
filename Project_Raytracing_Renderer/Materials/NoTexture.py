from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Materials.Material import Material


class NoTexture(Material):
    """
    Material without any characteristics just for giving a color without texture
    """
    def scatter(self, ray: Ray, intersection_point: Vector, normal_vector: Vector) -> tuple[Ray, Vector] | None:
        """
        Calculates how a ray is reflected

        :param ray: Ray that hits the object
        :param intersection_point: Point where the ray hits the object
        :param normal_vector: Normal vector at the point of intersection
        :return: None because no ray is reflected
        """
        return None
