from Project_Raytracing_Renderer.Ray import Ray
from Project_Raytracing_Renderer.Vector import Vector
from Project_Raytracing_Renderer.Image import Image


class Camera:
    def __init__(self, origin: Vector, focal_length: float, aspect_ratio: float, viewport_width: float) -> None:
        self.focal_length = focal_length
        self.aspect_ratio = aspect_ratio
        self.viewport_width = viewport_width
        self.viewport_height = self.viewport_width / self.aspect_ratio
        self.origin = origin
        self.horizontal = Vector(self.viewport_width, 0, 0)
        self.vertical = Vector(0, self.viewport_height, 0)
        self.lower_left_corner = (self.origin - self.horizontal / 2 -
                                  self.vertical / 2 - Vector(0, 0, self.focal_length))

    def render(self):
        width = 400
        height = int(width // self.aspect_ratio)
        image = Image(width, height)
        for j in range(height)[::-1]:
            for i in range(width):
                image.update(i, j, self.get_ray(i / (width - 1), j / (height - 1)).color())
        return image

    def get_ray(self, s: float, t: float) -> Ray:
        return Ray(self.origin, self.lower_left_corner + self.horizontal * s + self.vertical * t - self.origin)


if __name__ == '__main__':
    Camera(Vector(0, 0, 0), 1, 16 / 9, 3.555555555555555555555555555556).render().save_image('test.ppm')
