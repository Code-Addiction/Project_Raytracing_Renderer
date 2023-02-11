from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Materials.Material import Material
import math


class Sphere:
    """
    Sphere objects

    :param origin: Center of the sphere
    :param radius: Radius of the sphere
    :param material: Material of the sphere
    :param movement: Tuple of position to move to and start and end time of the movement or None if sphere does not move (default: None)
    """
    def __init__(self, origin: Vector, radius: float, material: Material,
                 movement: tuple[Vector, float, float] | None = None):
        self.origin = origin
        self.radius = radius
        self.material = material
        self.movement = movement

    def hits(self, ray: Ray, t_min: float, t_max: float) -> tuple[Vector, Vector, Material, float] | None:
        """
        Checks if ray hits this sphere

        :param ray: Ray to check
        :param t_min: Starting point of ray to check for intersection
        :param t_max: End point of ray to check for intersection
        :return: Tuple containing point of intersection, normal vector at that point, material and point of ray at which it hits the sphere or None if ray does not hit the sphere
        """
        oc = ray.origin - self.move(ray.time)
        a = ray.direction.length()**2
        half_b = oc * ray.direction
        c = oc.length()**2 - self.radius**2

        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return None

        sqrtd = math.sqrt(discriminant)

        root = (-half_b - sqrtd) / a

        if not t_min < root < t_max:
            root = (-half_b + sqrtd) / a
            if not t_min < root < t_max:
                return None

        intersection_point = ray.position(root)
        normal_vector = (intersection_point - self.move(ray.time)) / self.radius

        return intersection_point, normal_vector, self.material, root

    def move(self, time: float | None) -> Vector:
        """
        Calculates position of the sphere at a specific time

        :param time: Time to get position at or None
        :return: Position at that time
        """
        if self.movement is None or time is None:
            return self.origin

        target, time0, time1 = self.movement
        return self.origin + (target - self.origin) * ((time - time0) / (time1 - time0))
