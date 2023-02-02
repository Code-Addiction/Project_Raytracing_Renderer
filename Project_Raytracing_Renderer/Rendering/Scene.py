from __future__ import annotations

from Project_Raytracing_Renderer.Objects.Camera import Camera
from Project_Raytracing_Renderer.Objects.Sphere import Sphere
from Project_Raytracing_Renderer.Rendering.Image import Image
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Objects.World import World
from Project_Raytracing_Renderer import Materials


class Scene:
    def __init__(self, camera: Camera) -> None:
        self.camera = camera
        self.world = World()

    def add(self, sphere: Sphere | list) -> Scene:
        self.world.add(sphere)
        return self

    def render(self, width: int, render_depth: int) -> Image:
        return self.camera.render(width, render_depth, self.world)


if __name__ == '__main__':
    Scene(Camera(Vector(0, 0, 0),
                 1, 16 / 9,
                 3.555555555555555555555555555556, 16)).add([Sphere(Vector(0, -100.5, -1),
                                                                    100,
                                                                    Materials.Diffuse(Vector(0.8 * 255,
                                                                                             0.8 * 255,
                                                                                             0))),
                                                             Sphere(Vector(0, 0, -1),
                                                                    0.5, Materials.Diffuse(Vector(0.7 * 255,
                                                                                                  0.3 * 255,
                                                                                                  0.3 * 255))),
                                                             Sphere(Vector(-1, 0, -1),
                                                                    0.5, Materials.Specular(Vector(0.8 * 255,
                                                                                                   0.8 * 255,
                                                                                                   0.8 * 255),
                                                                                            0.3)),
                                                             Sphere(Vector(1, 0, -1),
                                                                    0.5, Materials.Specular(Vector(0.8 * 255,
                                                                                                   0.6 * 255,
                                                                                                   0.2 * 255)))
                                                             ]).render(600, 16).save_image('test.ppm', True)
