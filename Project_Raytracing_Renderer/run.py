#!/usr/bin/env python3
from Project_Raytracing_Renderer.Rendering.Scene import Scene
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Objects.Camera import Camera
from Project_Raytracing_Renderer.Objects.Sphere import Sphere
from Project_Raytracing_Renderer.Rendering.Image import Image
from Project_Raytracing_Renderer import Materials
import os
import json

# Conversion from JSON material to Python material class (with additional parameter)
MATERIAL_DICT = {'diffuse': (Materials.Diffuse, None),
                 'emissive': (Materials.Emissive, 'intensity'),
                 'no_texture': (Materials.NoTexture, None),
                 'specular': (Materials.Specular, 'fuzz'),
                 'transmissive': (Materials.Transmissive, 'refraction_index')}


def render_config(path: str) -> None:
    """
    Reads in config file, creates scene from it, renders it and saves resulting image

    :param path: Path of the config file
    """
    with open(path) as config_file:
        config = json.load(config_file)

    image_config = config.get('image')
    if image_config is not None:
        image = Image(image_config['width'],
                      image_config['height'],
                      Vector(*image_config['color']))
    else:
        camera_data = config['camera']
        time_interval = camera_data.get('time_interval')
        if time_interval is not None:
            time_interval = tuple(time_interval)

        camera = Camera(Vector(*camera_data['look_from']),
                        Vector(*camera_data['look_at']),
                        Vector(*camera_data['up']),
                        camera_data['vfov'],
                        camera_data['focal_length'],
                        camera_data['aspect_ratio'],
                        camera_data['viewport_height'],
                        camera_data['samples_per_pixel'],
                        time_interval
                        )

        background = config.get('background')
        if background is not None:
            background = Vector(*background)

        scene = Scene(camera, background)

        spheres = config.get('spheres', [])
        for sphere_config in spheres:
            material_config = sphere_config['material']
            material_type, parameter = MATERIAL_DICT[material_config['type']]
            if parameter is not None:
                material = material_type(Vector(*material_config['color']), material_config[parameter])
            else:
                material = material_type(Vector(*material_config['color']))

            movement = sphere_config.get('movement')
            if movement is not None:
                target, time0, time1 = tuple(movement)
                movement = (Vector(*target), time0, time1)

            sphere = Sphere(Vector(*sphere_config['origin']),
                            sphere_config['radius'],
                            material,
                            movement)
            scene.add(sphere)

        rendering_config = config['rendering']
        image = scene.render(rendering_config['width'],
                             rendering_config['render_depth'],
                             rendering_config['in_parallel'],
                             rendering_config.get('number_cores', 0))

    saving_config = config['saving']
    image.save_image(saving_config['path'],
                     saving_config['gamma_correct'])


def main() -> None:
    """
    Manages user interaction and reads in the path of the config file(s)
    """
    path = input("Please enter path of config file or 'all' for all files in config directory: ")
    if path.lower() == 'all':
        for path in os.listdir("configs/"):
            if path == 'example.json':
                continue
            render_config("configs/" + path)
    else:
        render_config(path)


if __name__ == '__main__':
    main()
