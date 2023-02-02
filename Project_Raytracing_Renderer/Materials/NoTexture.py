from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Rendering.Ray import Ray
from Project_Raytracing_Renderer.Materials.Material import Material


class NoTexture(Material):
    def scatter(self, ray: Ray, intersection_point: Vector, normal_vector: Vector) -> None:
        return None
