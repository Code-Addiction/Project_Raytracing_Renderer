from __future__ import annotations

import multiprocessing as mp
from Project_Raytracing_Renderer.Objects.World import World
from Project_Raytracing_Renderer.Objects.Camera import Camera
from Project_Raytracing_Renderer.Rendering.Vector import Vector


class RenderingProcess(mp.Process):
    """
    Process for rendering images in parallel

    :param width: Width of the resulting image
    :param render_depth: Render depth
    :param world: World instance containing all objects
    :param height_start: Row to start rendering (inclusive)
    :param height_end: Row to stop rendering (exclusive)
    :param camera: Camera to render with
    :param results: Array of the whole image to save results in
    :param background: Color of background or None (default: None)
    """
    def __init__(self, width: int, render_depth: int, world: World,
                 height_start: int, height_end: int, camera: Camera,
                 results: mp.Array, background: Vector | None = None):
        mp.Process.__init__(self)
        self._width = width
        self._render_depth = render_depth
        self._world = world
        self._height_start = height_start
        self._height_end = height_end
        self._camera = camera
        self._results = results
        self._background = background

    def run(self) -> None:
        """
        Runs the rendering with the given parameters on a new core
        """
        self._camera.render_parallel(self._width, self._render_depth, self._world,
                                     self._height_start, self._height_end, self._results,
                                     self._background)

