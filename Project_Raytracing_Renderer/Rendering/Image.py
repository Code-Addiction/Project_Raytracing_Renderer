from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Vector import Vector
import math
from multiprocessing import Array


class Image:
    def __init__(self, width: int, height: int, color: Vector = Vector(0, 0, 0), array: Array | None = None) -> None:
        self._height = height
        self._width = width
        if array is not None:
            self._array = array
            self._matrix = None
        else:
            self._array = None
            self._matrix = []
            for i in range(self._width):
                row = []
                for j in range(self._height):
                    row.append(color)
                self._matrix.append(row)

    def save_image(self, path: str, gamma_correct: bool = False):
        image_str = f'P3\n{self._width} {self._height}\n255'

        # To optimize the performance, the if clauses are put on the outside of the loop
        # This way, the code gets less clean because similar code is repeated multiple times,
        # but the if clauses only have to be checked once instead of in every loop iteration
        # and thus this code should be faster
        if self._array is not None and not gamma_correct:
            for j in range(self._height)[::-1]:
                for i in range(self._width):
                    index = (j * self._width + i) * 3
                    image_str = image_str + f'\n{self._array[index]} {self._array[index + 1]} ' \
                                            f'{self._array[index + 2]}'
        elif self._array is not None and gamma_correct:
            for j in range(self._height)[::-1]:
                for i in range(self._width):
                    index = (j * self._width + i) * 3
                    red = math.sqrt(self._array[index] / 255) * 255
                    green = math.sqrt(self._array[index + 1] / 255) * 255
                    blue = math.sqrt(self._array[index + 2] / 255) * 255
                    image_str = image_str + f'\n{int(red)} {int(green)} {int(blue)}'
        elif not gamma_correct:
            for j in range(self._height)[::-1]:
                for i in range(self._width):
                    red, green, blue = self._matrix[i][j].to_tuple()
                    image_str = image_str + f'\n{int(red)} {int(green)} {int(blue)}'
        else:
            for j in range(self._height)[::-1]:
                for i in range(self._width):
                    red, green, blue = self._matrix[i][j].to_tuple()
                    red = math.sqrt(red / 255) * 255
                    green = math.sqrt(green / 255) * 255
                    blue = math.sqrt(blue / 255) * 255
                    image_str = image_str + f'\n{int(red)} {int(green)} {int(blue)}'
        with open(path, mode='w+') as f:
            f.write(image_str)

    def update(self, i: int, j: int, color: Vector) -> None:
        if self._array is not None:
            index = (i * self._width + j) * 3
            self._array[index] = color.x
            self._array[index + 1] = color.y
            self._array[index + 2] = color.z
        else:
            self._matrix[i][j] = color

    @classmethod
    def from_array(cls, width: int, height: int, array) -> Image:
        image = Image(width, height)
        for j in range(height):
            for i in range(width):
                index = (j * width + i) * 3
                color = Vector(array[index], array[index + 1], array[index + 2])
                image.update(i, j, color)
        return image

    def __str__(self) -> str:
        if self._array is not None:
            return str(self._array)
        else:
            return str(self._matrix)
