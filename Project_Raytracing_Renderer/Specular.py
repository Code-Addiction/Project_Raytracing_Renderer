from Project_Raytracing_Renderer.Material import Material
from Project_Raytracing_Renderer.Ray import Ray
from Project_Raytracing_Renderer.Vector import Vector


class Specular(Material):
    def scatter(self, ray: Ray, intersection_point: Vector,
                normal_vector: Vector) -> tuple[Vector, Vector]:
        pass
