import numpy as np
from Project_Raytracing_Renderer.Vector import Vector


class Image:
    def __init__(self, width: int, height: int, color: Vector = Vector(0, 0, 0)) -> None:
        self._height = height
        self._width = width
        self._matrix = []
        for i in range(self._width):
            row = []
            for j in range(self._height):
                row.append(color)
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
        for j in range(self._height):
            for i in range(self._width):
                red, green, blue = self._matrix[i][j].to_tuple()
                image_str = image_str + f'\n{int(red)} {int(green)} {int(blue)}'
        with open(path, mode='w+') as f:
            f.write(image_str)

    def update(self, i: int, j: int, color: Vector, overwrite: bool = True) -> None:
        if overwrite:
            self._matrix[i][j] = color
        else:
            self._matrix[i][j] += color

    def __str__(self) -> str:
        return str(self._matrix)
