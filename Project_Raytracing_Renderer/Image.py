import numpy as np
from Project_Raytracing_Renderer.Vector import Vector
from Project_Raytracing_Renderer.Camera import Camera


class Image:
    def __init__(self, width: int, height: int) -> None:
        self._height = height
        self._width = width
        self._matrix = []
        for i in range(self._width):
            row = []
            for j in range(self._height):
                row.append(Vector(0, 0, 0))
            self._matrix.append(row)

    def to_numpy(self) -> np.ndarray:
        array = np.zeros(shape=(self._width, self._height, 3), dtype=np.uint8)
        for i in range(self._width):
            for j in range(self._height):
                red, green, blue = self._matrix[i][j].to_tuple()
                array[i][j][0] = red
                array[i][j][1] = green
                array[i][j][2] = blue
        return array

    def save_image(self, path: str):
        image_str = f'P3\n{self._width} {self._height}\n255'
        for i in range(self._width):
            for j in range(self._height):
                red, green, blue = self._matrix[i][j].to_tuple()
                image_str = image_str + f'\n{red} {green} {blue}'
        with open(path, mode='w+') as f:
            f.write(image_str)

    def render(self, camera):
        for j in range(self._height)[::-1]:
            for i in range(self._width):
                self._matrix[i][j] = camera.get_ray(i / (self._width - 1), j / (self._height - 1)).color()

    def __str__(self) -> str:
        return str(self._matrix)


if __name__ == '__main__':
    cam = Camera(Vector(0, 0, 0), 1, 16 / 9, 3.555555555556)
    img = Image(400, int(400 // (16 / 9)))
    img.render(cam)
    img.save_image('test.ppm')
