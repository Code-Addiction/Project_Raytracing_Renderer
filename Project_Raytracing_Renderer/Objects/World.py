from __future__ import annotations

from Project_Raytracing_Renderer.Objects.Sphere import Sphere
from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer import Materials


class World:
    """
    Abstraction of all the objects in a scene (can be iterated)
    """
    def __init__(self):
        self.objects = []
        self._current_index = 0

    def add(self, sphere: Sphere | list) -> None:
        """
        Add sphere or spheres to scene

        :param sphere: Sphere or list of spheres to add
        """
        if type(sphere) is list:
            for sph in sphere:
                self.objects.append(sph)
        else:
            self.objects.append(sphere)

    def __iter__(self) -> World:
        """
        Makes the World object iterable
        """
        self._current_index = 0
        return self

    def __next__(self):
        """
        Returns next object
        """
        if self._current_index < len(self.objects):
            current_object = self.objects[self._current_index]
            self._current_index = self._current_index + 1
            return current_object
        raise StopIteration

    def hits(self, ray: Ray, t_min: float, t_max: float) -> tuple[Vector, Vector, Materials.Material, float] | None:
        """
        Checks if ray hits any object in scene

        :param ray: Ray to check
        :param t_min: Starting point of ray to check for intersection
        :param t_max: End point of ray to check for intersection
        :return: Tuple containing point of intersection, normal vector at that point, material and point of ray at which it hits any sphere or None if ray does not hit anything
        """
        closest_yet = t_max
        result = None

        for scene_object in self.objects:
            tmp_result = scene_object.hits(ray, t_min, closest_yet)
            if tmp_result is not None:
                _, _, _, closest_yet = tmp_result
                result = tmp_result

        return result
