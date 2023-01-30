from Project_Raytracing_Renderer.Vector import Vector
from Project_Raytracing_Renderer.Ray import Ray


class Material:
    def __init__(self, color: Vector) -> None:
        self.color = color

    def scatter(self, ray: Ray, intersection_point: Vector, normal_vector: Vector) -> tuple[Vector, Vector]:
        raise NotImplementedError
