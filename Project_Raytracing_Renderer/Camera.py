from __future__ import annotations

from Project_Raytracing_Renderer.Ray import Ray
from Project_Raytracing_Renderer.Vector import Vector
from Project_Raytracing_Renderer.Image import Image
from Project_Raytracing_Renderer.Sphere import Sphere
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

    def render(self, objects: list):
        width = 400
        height = int(width // self.aspect_ratio)
        image = Image(width, height)
        for j in range(height)[::-1]:
            for i in range(width):
                final_color = Vector(0, 0, 0)
                for _ in range(self.samples_per_pixel):
                    _, set_color, set_t = Camera.get_color(self.get_ray(i / (width - 1), j / (height - 1)), None)
                    u = (i + np.random.uniform()) / (width - 1)
                    v = (j + np.random.uniform()) / (height - 1)
                    for sphere in objects:
                        hit, color, t = Camera.get_color(
                            self.get_ray(u, v), sphere)
                        if hit and t < set_t:
                            set_t = t
                            set_color = color
                    final_color = final_color + set_color
                image.update(i, j, final_color / self.samples_per_pixel)
        return image

    def get_ray(self, s: float, t: float) -> Ray:
        return Ray(self.origin, self.lower_left_corner + self.horizontal * s + self.vertical * t - self.origin)

    @staticmethod
    def get_color(ray: Ray, sphere: Sphere | None) -> tuple[bool, Vector, float]:
        if sphere is not None:
            result = sphere.hits(ray)
            if result is not None:
                _, _, color, t = result
                return True, color, t

        unit_direction = ray.direction.normalize()
        t = 0.5 * (unit_direction.y + 1)
        return False, Vector(255, 255, 255) * (1 - t) + Vector(0.5 * 255, 0.7 * 255, 255) * t, float('inf')
