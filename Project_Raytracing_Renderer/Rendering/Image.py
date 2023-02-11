from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Vector import Vector
import math
from multiprocessing import Array


class Image:
    """
    Representation of a rendered image

    :param width: Width of the image
    :param height: Height of the image
    :param color: Color to initialise the image with (default: black)
    :param array: Array representation of the image or None (default: None)
    """
    def __init__(self, width: int, height: int, color: Vector = Vector(0, 0, 0), array: Array | None = None):
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

    def save_image(self, path: str, gamma_correct: bool = False) -> None:
        """
        Saves the image

        :param path: Path to save image to
        :param gamma_correct: If image should be gamma corrected before saving (default: False)
        """
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
        """
        Updates color of a pixel

        :param i: Width index of pixel
        :param j: Height index of pixel
        :param color: Color to write to image
        """
        if self._array is not None:
            index = (i * self._width + j) * 3
            self._array[index] = color.x
            self._array[index + 1] = color.y
            self._array[index + 2] = color.z
        else:
            self._matrix[i][j] = color

    def __str__(self) -> str:
        """
        Converts image to string for printing

        :return: String representation of image
        """
        if self._array is not None:
            return str(self._array)
        else:
            return str(self._matrix)
