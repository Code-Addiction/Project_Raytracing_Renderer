from Project_Raytracing_Renderer.Materials.Material import Material
from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Rendering.Vector import Vector


class Specular(Material):
    def scatter(self, ray: Ray, intersection_point: Vector,
                normal_vector: Vector) -> tuple[Vector, Vector]:
        pass
