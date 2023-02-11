from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Image import Image
from Project_Raytracing_Renderer.Objects.World import World
from Project_Raytracing_Renderer.Materials.NoTexture import NoTexture
import numpy as np
import random
import math
from multiprocessing import RawArray as Array


class Camera:
    """
    Camera for defining point of view and handling of the rendering

    :param look_from: Position of the camera
    :param look_at: Where the camera should look at
    :param up: Orientation of the camera
    :param vfov: Vertical angle of the camera's field of view
    :param focal_length: Distance from camera to canvas (on which the image shall be projected)
    :param aspect_ratio: Aspect ratio of the resulting image
    :param viewport_height: Height of the canvas
    :param samples_per_pixel: Number of rays used per pixel
    :param time_interval: Tuple of virtual start and end time of rendering or None if no motion should be capture (default: None)
    """
    def __init__(self, look_from: Vector, look_at: Vector, up: Vector,
                 vfov: float, focal_length: float,
                 aspect_ratio: float, viewport_height: float,
                 samples_per_pixel: int, time_interval: tuple[float, float] | None = None):
        self.focal_length = focal_length
        self.aspect_ratio = aspect_ratio
        self.viewport_height = viewport_height * math.tan(math.radians(vfov) / 2)
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.origin = look_from
        self.w = (look_from - look_at).normalize()
        self.u = Vector.cross_product(up, self.w).normalize()
        self.v = Vector.cross_product(self.w, self.u)
        self.horizontal = self.u * self.viewport_width
        self.vertical = self.v * self.viewport_height
        self.lower_left_corner = (self.origin - self.horizontal / 2 -
                                  self.vertical / 2 - self.w)
        self.samples_per_pixel = samples_per_pixel
        self.time_interval = time_interval

    def render(self, width: int, render_depth: int, world: World, background: Vector | None = None) -> Image:
        """
        Renders the scene

        :param width: Width of the resulting image
        :param render_depth: Render depth
        :param world: World instance containing all objects
        :param background: Color of background or None (default: None)
        :return: Rendered image
        """
        height = int(width // self.aspect_ratio)
        image = Image(width, height)
        for j in range(height)[::-1]:
            for i in range(width):
                pixel_color = Vector(0, 0, 0)
                if self.samples_per_pixel == 1:
                    u = i / (width - 1)
                    v = j / (height - 1)
                    pixel_color = Camera.get_color(self.get_ray(u, v), world, render_depth, background)
                else:
                    for _ in range(self.samples_per_pixel):
                        u = (i + np.random.uniform()) / (width - 1)
                        v = (j + np.random.uniform()) / (height - 1)
                        pixel_color = pixel_color + Camera.get_color(self.get_ray(u, v), world,
                                                                     render_depth, background)
                    pixel_color = pixel_color / self.samples_per_pixel
                image.update(i, j, pixel_color)
        return image

    def render_parallel(self, width: int, render_depth: int, world: World,
                        height_start: int, height_end: int, output_array: Array,
                        background: Vector | None = None) -> None:
        """
        Renders a section of the scene

        :param width: Width of the resulting image
        :param render_depth: Render depth
        :param world: World instance containing all objects
        :param height_start: Row to start rendering (inclusive)
        :param height_end: Row to stop rendering (exclusive)
        :param output_array: Array of the whole image to save results in
        :param background: Color of background or None (default: None)
        """
        height = int(width // self.aspect_ratio)
        for j in range(height_start, height_end)[::-1]:
            index = j * width * 3
            for i in range(width):
                pixel_color = Vector(0, 0, 0)
                if self.samples_per_pixel == 1:
                    u = i / (width - 1)
                    v = j / (height - 1)
                    pixel_color = Camera.get_color(self.get_ray(u, v), world, render_depth, background)
                else:
                    for _ in range(self.samples_per_pixel):
                        u = (i + np.random.uniform()) / (width - 1)
                        v = (j + np.random.uniform()) / (height - 1)
                        pixel_color = pixel_color + Camera.get_color(self.get_ray(u, v), world,
                                                                     render_depth, background)
                    pixel_color = pixel_color / self.samples_per_pixel

                output_array[index] = int(pixel_color.x)
                output_array[index + 1] = int(pixel_color.y)
                output_array[index + 2] = int(pixel_color.z)
                index = index + 3

    def get_ray(self, s: float, t: float) -> Ray:
        """
        Calculates ray from camera to pixel defined by s and t

        :param s: Relative width position of the pixel, normalized to image width (between 0 and 1)
        :param t: Relative height position of the pixel, normalized to image height (between 0 and 1)
        :return: Ray from camera through pixel
        """
        if self.time_interval is not None:
            time0, time1 = self.time_interval
            return Ray(self.origin, self.lower_left_corner + self.horizontal * s + self.vertical * t - self.origin,
                       random.uniform(time0, time1))
        return Ray(self.origin, self.lower_left_corner + self.horizontal * s + self.vertical * t - self.origin)

    @staticmethod
    def get_color(ray: Ray, world: World, max_depth: int, background: Vector | None = None) -> Vector:
        """
        Computes the color of the given ray

        :param ray: Ray to compute color of
        :param world: World instance containing all objects
        :param max_depth: Render depth
        :param background: Color of background or None (default: None)
        :return: Color of the ray
        """
        if max_depth < 1:
            return Vector(0, 0, 0)

        result = world.hits(ray, 0.001, float('inf'))
        if result is not None:
            intersection_point, normal_vector, material, _ = result
            emitted = material.emit()
            material_result = material.scatter(ray, intersection_point, normal_vector)
            if material_result is not None:
                scattered, attenuation = material_result
                return emitted + attenuation.modulate(Camera.get_color(scattered, world, max_depth - 1, background))
            elif type(material) == NoTexture:
                return material.color
            return emitted

        if background is not None:
            return background
        else:
            unit_direction = ray.direction.normalize()
            t = 0.5 * (unit_direction.y + 1)
            return Vector(255, 255, 255) * (1 - t) + Vector(127.5, 178.5, 255) * t
