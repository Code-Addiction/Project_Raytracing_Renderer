from __future__ import annotations

from Project_Raytracing_Renderer.Camera import Camera
from Project_Raytracing_Renderer.Sphere import Sphere
from Project_Raytracing_Renderer.Image import Image
from Project_Raytracing_Renderer.Vector import Vector


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

    def render(self) -> Image:
        return self.camera.render(self.objects)


if __name__ == '__main__':
    Scene(Camera(Vector(0, 0, 0),
                 1, 16 / 9,
                 3.555555555555555555555555555556)).add([Sphere(Vector(1, 1, -2),
                                                                1, Vector(255,
                                                                          0, 0)),
                                                         Sphere(Vector(-2, 0, -4),
                                                                2, Vector(0,
                                                                          255, 0)),
                                                         Sphere(Vector(0, -1, -3),
                                                                1.5, Vector(0,
                                                                            0, 255)),
                                                         Sphere(Vector(1.25, 0.6, -1.3),
                                                                0.4, Vector(0,
                                                                            0, 0)),
                                                         Sphere(Vector(3.5, 0, -2),
                                                                2, Vector(255,
                                                                          255, 255))

                                                         ]).render().save_image('test.ppm')
