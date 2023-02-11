from __future__ import annotations

from Project_Raytracing_Renderer.Objects.Camera import Camera
from Project_Raytracing_Renderer.Objects.Sphere import Sphere
from Project_Raytracing_Renderer.Rendering.Image import Image
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Objects.World import World
from Project_Raytracing_Renderer.Rendering.RenderingProcess import RenderingProcess
import multiprocessing as mp


class Scene:
    """
    Interface to interact with the scene with

    :param camera: Camera for rendering
    :param background: Color of background or None (default: None)
    """
    def __init__(self, camera: Camera, background: Vector | None = None):
        self.camera = camera
        self.world = World()
        self.background = background

    def add(self, sphere: Sphere | list) -> Scene:
        """
        Add sphere or spheres to scene

        :param sphere: Sphere or list of spheres to add
        :return: The updated scene
        """
        self.world.add(sphere)
        return self

    def render(self, width: int, render_depth: int, in_parallel: bool = True, number_cores: int = 0) -> Image:
        """
        Render the scene

        :param width: Width of the resulting image
        :param render_depth: Render depth
        :param in_parallel: If the rendering should be done in parallel (default: True)
        :param number_cores: Number of cores to render on, 0 means max available number of cores (default: 0)
        :return: Rendered image
        """
        if not in_parallel:
            return self.camera.render(width, render_depth, self.world, self.background)

        max_cores = mp.cpu_count()
        if not 0 < number_cores <= max_cores:
            number_cores = max_cores

        processes = []

        height = int(width // self.camera.aspect_ratio)
        rows_per_process = int(height // number_cores)

        results = mp.RawArray('B', height * width * 3)

        for i in range(number_cores - 1):
            process = RenderingProcess(width, render_depth, self.world,
                                       i * rows_per_process, (i + 1) * rows_per_process,
                                       self.camera, results, self.background)
            processes.append(process)
            process.start()

        height_start = (number_cores - 1) * rows_per_process
        self.camera.render_parallel(width, render_depth, self.world, height_start,
                                    height, results, self.background)

        for process in processes:
            process.join()

        return Image(width, height, array=results)
