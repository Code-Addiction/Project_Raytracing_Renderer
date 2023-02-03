from __future__ import annotations

from Project_Raytracing_Renderer.Objects.Camera import Camera
from Project_Raytracing_Renderer.Objects.Sphere import Sphere
from Project_Raytracing_Renderer.Rendering.Image import Image
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Objects.World import World
from Project_Raytracing_Renderer.Rendering.RenderingProcess import RenderingProcess
from Project_Raytracing_Renderer import Materials
import multiprocessing as mp
import time


class Scene:
    def __init__(self, camera: Camera) -> None:
        self.camera = camera
        self.world = World()

    def add(self, sphere: Sphere | list) -> Scene:
        self.world.add(sphere)
        return self

    def render(self, width: int, render_depth: int, in_parallel: bool = False, number_cores: int = 0) -> Image:
        if not in_parallel:
            return self.camera.render(width, render_depth, self.world)

        max_cores = mp.cpu_count()
        if not 0 < number_cores <= max_cores:
            number_cores = max_cores

        processes = []

        height = int(width // self.camera.aspect_ratio)
        rows_per_process = int(height // number_cores)

        results = mp.Array('B', height * width * 3)

        for i in range(number_cores - 1):
            process = RenderingProcess(width, render_depth, self.world,
                                       i * rows_per_process, (i + 1) * rows_per_process,
                                       self.camera, results)
            processes.append(process)
            process.start()

        height_start = (number_cores - 1) * rows_per_process
        self.camera.render_parallel(width, render_depth, self.world, height_start, height, results)

        for process in processes:
            process.join()

        return Image(width, height, array=results)


if __name__ == '__main__':
    start_time = time.time_ns()
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
                                                             ]).render(600, 16, False).save_image('test_ser.ppm', True)
    end_time = time.time_ns()
    print("Serial took:", end_time - start_time)

    start_time = time.time_ns()
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
                                                             ]).render(600, 16, True).save_image('test_par.ppm', True)
    end_time = time.time_ns()
    print("Parallel took:", end_time - start_time)
