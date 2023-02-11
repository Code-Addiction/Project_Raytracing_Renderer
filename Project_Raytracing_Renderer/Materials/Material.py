from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Ray import Ray
import math


class Material:
    """
    Abstract parent class for materials

    :param color: Color of the material
    """
    def __init__(self, color: Vector):
        self.color = color

    def scatter(self, ray: Ray, intersection_point: Vector, normal_vector: Vector) -> tuple[Ray, Vector] | None:
        """
        Calculates how a ray is reflected/refracted

        :param ray: Ray that hits the object
        :param intersection_point: Point where the ray hits the object
        :param normal_vector: Normal vector at the point of intersection
        :return: Either the reflected/refracted ray and the material's color or None if no ray is reflected
        """
        raise NotImplementedError

    def emit(self) -> Vector:
        """
        Determines emitted color

        :return: Emitted color
        """
        return Vector(0, 0, 0)

    @staticmethod
    def reflect(direction: Vector, normal_vector: Vector) -> Vector:
        """
        Calculates the direction of the reflected ray

        :param direction: Normalized direction of the hitting ray
        :param normal_vector: Normal vector at the point of intersection
        :return: Direction of reflected ray
        """
        return direction - normal_vector * (direction * normal_vector) * 2

    @staticmethod
    def refract(direction: Vector, normal_vector: Vector, refraction_ratio: float, factor: int) -> Vector:
        """
        Calculates the direction of the refracted ray

        :param direction: Normalized direction of the hitting ray
        :param normal_vector: Normal vector at the point of intersection
        :param refraction_ratio: Refraction ratio of the material
        :param factor: -1 if normal vector and direction of ray are in the same direction otherwise 1
        :return: Direction of refracted ray
        """
        cos_theta = min(direction * normal_vector * -1 * factor, 1)
        ray_perp = (direction + normal_vector * cos_theta * factor) * refraction_ratio
        ray_parl = normal_vector * -math.sqrt(math.fabs(1 - ray_perp.length() ** 2)) * factor

        return ray_perp + ray_parl
