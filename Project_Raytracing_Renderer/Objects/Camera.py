from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Image import Image
from Project_Raytracing_Renderer.Objects.Sphere import Sphere
from Project_Raytracing_Renderer.Materials.NoTexture import NoTexture
import numpy as np


class Camera:
    def __init__(self, origin: Vector, focal_length: float,
                 aspect_ratio: float, viewport_width: float,
                 samples_per_pixel: int) -> None:
        self.focal_length = focal_length
        self.aspect_ratio = aspect_ratio
        self.viewport_width = viewport_width
        self.viewport_height = self.viewport_width / self.aspect_ratio
        self.origin = origin
        self.horizontal = Vector(self.viewport_width, 0, 0)
        self.vertical = Vector(0, self.viewport_height, 0)
        self.lower_left_corner = (self.origin - self.horizontal / 2 -
                                  self.vertical / 2 - Vector(0, 0, self.focal_length))
        self.samples_per_pixel = samples_per_pixel

    def render(self, width: int, render_depth: int, objects: list):
        height = int(width // self.aspect_ratio)
        image = Image(width, height)
        for j in range(height)[::-1]:
            for i in range(width):
                if self.samples_per_pixel == 1:
                    u = i / (width - 1)
                    v = j / (height - 1)
                    _, set_color, set_t = Camera.get_color(self.get_ray(u, v), None, 1)
                    for sphere in objects:
                        hit, color, t = Camera.get_color(
                            self.get_ray(u, v), sphere,
                            render_depth)
                        if hit and t < set_t:
                            set_t = t
                            set_color = color
                    image.update(i, j, set_color)
                else:
                    final_color = Vector(0, 0, 0)
                    for _ in range(self.samples_per_pixel):
                        _, set_color, set_t = Camera.get_color(self.get_ray(i / (width - 1), j / (height - 1)), None, 1)
                        u = (i + np.random.uniform()) / (width - 1)
                        v = (j + np.random.uniform()) / (height - 1)
                        for sphere in objects:
                            hit, color, t = Camera.get_color(
                                self.get_ray(u, v), sphere,
                                render_depth)
                            if hit and t < set_t:
                                set_t = t
                                set_color = color
                        final_color = final_color + set_color
                    image.update(i, j, final_color / self.samples_per_pixel)
        return image

    def get_ray(self, s: float, t: float) -> Ray:
        return Ray(self.origin, self.lower_left_corner + self.horizontal * s + self.vertical * t - self.origin)

    @staticmethod
    def get_color(ray: Ray, sphere: Sphere | None, max_depth: int) -> tuple[bool, Vector, float]:
        if max_depth < 1:
            return False, Vector(0, 0, 0), float('inf')

        if sphere is not None:
            result = sphere.hits(ray)
            if result is not None:
                intersection_point, normal_vector, material, t = result
                direction, material_color = material.scatter(ray, intersection_point, normal_vector)
                if type(material) == NoTexture:
                    return True, material_color, t
                _, color, _ = Camera.get_color(Ray(intersection_point, direction), sphere, max_depth - 1)
                return True, color.modulate(material_color), t

        unit_direction = ray.direction.normalize()
        t = 0.5 * (unit_direction.y + 1)
        return False, Vector(255, 255, 255) * (1 - t) + Vector(0.5 * 255, 0.7 * 255, 255) * t, float('inf')
