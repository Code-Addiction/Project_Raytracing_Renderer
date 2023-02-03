import multiprocessing as mp
from Project_Raytracing_Renderer.Objects.World import World
from Project_Raytracing_Renderer.Objects.Camera import Camera


class RenderingProcess(mp.Process):
    def __init__(self, width: int, render_depth: int, world: World,
                 height_start: int, height_end: int, camera: Camera, results: mp.Array):
        mp.Process.__init__(self)
        self._width = width
        self._render_depth = render_depth
        self._world = world
        self._height_start = height_start
        self._height_end = height_end
        self._camera = camera
        self._results = results

    def run(self) -> None:
        self._camera.render_parallel(self._width, self._render_depth, self._world,
                                     self._height_start, self._height_end, self._results)

