from __future__ import annotations

from Project_Raytracing_Renderer.Objects.Camera import Camera
from Project_Raytracing_Renderer.Objects.Sphere import Sphere
from Project_Raytracing_Renderer.Rendering.Image import Image
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Materials.Diffuse import Diffuse


class Scene:
    def __init__(self, camera: Camera) -> None:
        self.camera = camera
        self.objects = []

    def add(self, sphere: Sphere | list) -> Scene:
        if type(sphere) is list:
            for sph in sphere:
                self.objects.append(sph)
        else:
            self.objects.append(sphere)
        return self

    def render(self, width: int, render_depth: int) -> Image:
        return self.camera.render(width, render_depth, self.objects)


if __name__ == '__main__':
    Scene(Camera(Vector(0, 0, 0),
                 1, 16 / 9,
                 3.555555555555555555555555555556, 4)).add([Sphere(Vector(1, 1, -2),
                                                                   1, Diffuse(Vector(255,
                                                                                     0, 0))),
                                                            Sphere(Vector(-2, 0, -4),
                                                                   2, Diffuse(Vector(0,
                                                                                     255, 0))),
                                                            Sphere(Vector(0, -1, -3),
                                                                   1.5, Diffuse(Vector(0,
                                                                                       0, 255))),
                                                            Sphere(Vector(1.25, 0.6, -1.3),
                                                                   0.4, Diffuse(Vector(0,
                                                                                       0, 0))),
                                                            Sphere(Vector(3.5, 0, -2),
                                                                   2, Diffuse(Vector(255,
                                                                                     255, 255)))
                                                            ]).render(400, 4).save_image('test2.ppm')
