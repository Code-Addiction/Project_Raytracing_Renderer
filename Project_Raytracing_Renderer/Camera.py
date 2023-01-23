from Project_Raytracing_Renderer.Ray import Ray
from Project_Raytracing_Renderer.Vector import Vector


class Camera:
    def __init__(self, origin: Vector, focal_length: float, aspect_ratio: float, viewport_width: float) -> None:
        self.focal_length = focal_length
        self.aspect_ratio = aspect_ratio
        self.viewport_width = viewport_width
        self.viewport_height = self.viewport_width / self.aspect_ratio
        print('Height: ', self.viewport_height)
        print('Width: ', self.viewport_width)
        self.origin = origin
        self.horizontal = Vector(self.viewport_width, 0, 0)
        self.vertical = Vector(0, self.viewport_height, 0)
        self.lower_left_corner = (self.origin - self.horizontal / 2 -
                                  self.vertical / 2 - Vector(0, 0, self.focal_length))

    def get_ray(self, s: float, t: float) -> Ray:
        return Ray(self.origin, self.lower_left_corner + self.horizontal * s + self.vertical * t - self.origin)
