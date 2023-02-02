from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Image import Image
from Project_Raytracing_Renderer.Objects.World import World
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

    def render(self, width: int, render_depth: int, world: World) -> Image:
        height = int(width // self.aspect_ratio)
        image = Image(width, height)
        for j in range(height)[::-1]:
            for i in range(width):
                pixel_color = Vector(0, 0, 0)
                if self.samples_per_pixel == 1:
                    u = i / (width - 1)
                    v = j / (height - 1)
                    pixel_color = Camera.get_color(self.get_ray(u, v), world, render_depth)
                else:
                    for _ in range(self.samples_per_pixel):
                        u = (i + np.random.uniform()) / (width - 1)
                        v = (j + np.random.uniform()) / (height - 1)
                        pixel_color = pixel_color + Camera.get_color(self.get_ray(u, v), world, render_depth)
                    pixel_color = pixel_color / self.samples_per_pixel
                image.update(i, j, pixel_color)
        return image

    def get_ray(self, s: float, t: float) -> Ray:
        return Ray(self.origin, self.lower_left_corner + self.horizontal * s + self.vertical * t - self.origin)

    @staticmethod
    def get_color(ray: Ray, world: World, max_depth: int) -> Vector:
        if max_depth < 1:
            return Vector(0, 0, 0)

        result = world.hits(ray, 0.001, float('inf'))
        if result is not None:
            intersection_point, normal_vector, material, _ = result
            material_result = material.scatter(ray, intersection_point, normal_vector)
            if material_result is not None:
                scattered, attenuation = material_result
                return attenuation.modulate(Camera.get_color(scattered, world, max_depth - 1))
            elif type(material) == NoTexture:
                return material.color
            return Vector(0, 0, 0)

        unit_direction = ray.direction.normalize()
        t = 0.5 * (unit_direction.y + 1)
        return Vector(255, 255, 255) * (1 - t) + Vector(127.5, 178.5, 255) * t
