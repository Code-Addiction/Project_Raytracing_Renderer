from __future__ import annotations

from Project_Raytracing_Renderer.Rendering.Image import Image
from Project_Raytracing_Renderer.Rendering.Vector import Vector
from Project_Raytracing_Renderer.Objects.Camera import Camera
from Project_Raytracing_Renderer.Rendering.Scene import Scene
from Project_Raytracing_Renderer.Objects.Sphere import Sphere
from Project_Raytracing_Renderer import Materials
import argparse


DEFAULT_SPHERES = {0: (1, 1, -2, 1, 255, 0, 0),
                   1: (-2, 0, -4, 2, 0, 255, 0),
                   2: (0, -1, -3, 1.5, 0, 0, 255),
                   3: (1.25, 0.6, -1.3, 0.4, 0, 0, 0),
                   4: (3.5, 0, -2, 2, 255, 255, 255)}


def step1(path: str, width: int, height: int, gamma_correction: bool) -> None:
    red, green, blue = 0, 0, 0

    successful_input = False
    while not successful_input:
        red = input("Red (default: 128): ")
        if red == '':
            red = 128
        green = input("Green (default: 64): ")
        if green == '':
            green = 64
        blue = input("Blue (default: 255): ")
        if blue == '':
            blue = 255
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            print("Only integers are valid as a color")
            continue
        if red > 255 or red < 0 or green > 255 or green < 0 or blue > 255 or blue < 0:
            print("Colors can only be between 0 and 255")
            continue
        successful_input = True

    color = Vector(red, green, blue)
    image = Image(width, height, color)
    image.save_image(path, gamma_correction)


def step2(path: str, width: int, height: int, gamma_correction: bool) -> None:
    focal_length, viewport_width, samples_per_pixel = 0, 0, 1

    successful_input = False
    while not successful_input:
        focal_length = input("Focal length (default: 1.0): ")
        if focal_length == '':
            focal_length = 1
        viewport_width = input("Viewport width (default: 3.555555555555555555555555555556): ")
        if viewport_width == '':
            viewport_width = 3.555555555555555555555555555556
        try:
            focal_length = float(focal_length)
            viewport_width = float(viewport_width)
        except ValueError:
            print("Only floats are valid")
            continue
        successful_input = True

    camera = Camera(Vector(0, 0, 0),
                    focal_length,
                    width / height,
                    viewport_width,
                    samples_per_pixel)
    scene = Scene(camera)
    image = scene.render(width, 1)
    image.save_image(path, gamma_correction)


def step3(path: str, width: int, height: int, gamma_correction: bool) -> None:
    focal_length, viewport_width, samples_per_pixel, render_depth = 0, 0, 1, 1

    successful_input = False
    while not successful_input:
        focal_length = input("Focal length (default: 1.0): ")
        if focal_length == '':
            focal_length = 1
        viewport_width = input("Viewport width (default: 3.555555555555555555555555555556): ")
        if viewport_width == '':
            viewport_width = 3.555555555555555555555555555556
        try:
            focal_length = float(focal_length)
            viewport_width = float(viewport_width)
        except ValueError:
            print("Only floats are valid")
            continue
        successful_input = True

    camera = Camera(Vector(0, 0, 0),
                    focal_length,
                    width / height,
                    viewport_width,
                    samples_per_pixel)
    scene = Scene(camera)

    number_spheres = -1
    successful_input = False
    while not successful_input:
        number_spheres = input("Number of spheres to add (default: 5): ")
        if number_spheres == '':
            number_spheres = 5
        try:
            number_spheres = int(number_spheres)
        except ValueError:
            print("Only an integer is valid")
            continue
        successful_input = True

    spheres = []
    for i in range(number_spheres):
        x, y, z, radius, red, green, blue = 0, 0, 0, 0, 0, 0, 0

        print(f"\nInputs for sphere {i + 1}:")

        if DEFAULT_SPHERES.get(i) is not None:
            (default_x, default_y, default_z,
             default_radius, default_red, default_green,
             default_blue) = DEFAULT_SPHERES.get(i)
            successful_input = False
            while not successful_input:
                x = input(f"Position x (default: {default_x}): ")
                y = input(f"Position y (default: {default_y}): ")
                z = input(f"Position z (default: {default_z}): ")
                radius = input(f"Radius (default: {default_radius}): ")
                red = input(f"Red (default: {default_red}): ")
                green = input(f"Green (default: {default_green}): ")
                blue = input(f"Blue (default: {default_blue}): ")
                if x == '':
                    x = default_x
                if y == '':
                    y = default_y
                if z == '':
                    z = default_z
                if radius == '':
                    radius = default_radius
                if red == '':
                    red = default_red
                if green == '':
                    green = default_green
                if blue == '':
                    blue = default_blue
                try:
                    x = float(x)
                    y = float(y)
                    z = float(z)
                    radius = float(radius)
                    red = int(red)
                    green = int(green)
                    blue = int(blue)
                except ValueError:
                    print("Only integer are valid for the colors and floats for the rest")
                    continue
                if red > 255 or red < 0 or green > 255 or green < 0 or blue > 255 or blue < 0:
                    print("Colors can only be between 0 and 255")
                    continue
                if radius <= 0:
                    print("Radius has to be bigger than 0")
                    continue
                successful_input = True
        else:
            successful_input = False
            while not successful_input:
                x = input("Position x: ")
                y = input("Position y: ")
                z = input("Position z: ")
                radius = input("Radius: ")
                red = input("Red: ")
                green = input("Green: ")
                blue = input("Blue: ")
                try:
                    x = float(x)
                    y = float(y)
                    z = float(z)
                    radius = float(radius)
                    red = int(red)
                    green = int(green)
                    blue = int(blue)
                except ValueError:
                    print("Only integer are valid for the colors and floats for the rest")
                    continue
                if red > 255 or red < 0 or green > 255 or green < 0 or blue > 255 or blue < 0:
                    print("Colors can only be between 0 and 255")
                    continue
                if radius <= 0:
                    print("Radius has to be bigger than 0")
                    continue
                successful_input = True

        sphere = Sphere(Vector(x, y, z), radius, Materials.NoTexture(Vector(red, green, blue)))
        spheres.append(sphere)

    scene.add(spheres)
    image = scene.render(width, render_depth)
    image.save_image(path, gamma_correction)


def step4(path: str, width: int, height: int, gamma_correction: bool) -> None:
    focal_length, viewport_width, samples_per_pixel, render_depth = 0, 0, 0, 1
    number_images = 0
    samples_per_pixel_default = [1, 2, 4, 8, 16]

    successful_input_number_images = False
    while not successful_input_number_images:
        number_images = input("How many images do you want to render (default: 5): ")
        if number_images == '':
            number_images = 5
        try:
            number_images = int(number_images)
        except ValueError:
            print("Only an integer is valid")
            continue
        successful_input_number_images = True

    for j in range(number_images):
        if j > 0:
            path = input(f"\n\nPath for rendered image {j + 1}: ")

        successful_input = False
        while not successful_input:
            focal_length = input("Focal length (default: 1.0): ")
            if focal_length == '':
                focal_length = 1
            viewport_width = input("Viewport width (default: 3.555555555555555555555555555556): ")
            if viewport_width == '':
                viewport_width = 3.555555555555555555555555555556
            if j < len(samples_per_pixel_default):
                samples_per_pixel = input(
                    f"How many rays per pixel for image {j + 1} (default: {samples_per_pixel_default[j]}): ")
                if samples_per_pixel == '':
                    samples_per_pixel = samples_per_pixel_default[j]
            else:
                samples_per_pixel = input(f"How many rays per pixel for image {j + 1}: ")
            try:
                focal_length = float(focal_length)
                viewport_width = float(viewport_width)
                samples_per_pixel = int(samples_per_pixel)
            except ValueError:
                print("Only an integer is valid for the number of rays per pixel and only floats for the rest")
                continue
            successful_input = True

        camera = Camera(Vector(0, 0, 0),
                        focal_length,
                        width / height,
                        viewport_width,
                        samples_per_pixel)
        scene = Scene(camera)

        number_spheres = -1
        successful_input = False
        while not successful_input:
            number_spheres = input("Number of spheres to add (default: 5): ")
            if number_spheres == '':
                number_spheres = 5
            try:
                number_spheres = int(number_spheres)
            except ValueError:
                print("Only an integer is valid")
                continue
            successful_input = True

        spheres = []
        for i in range(number_spheres):
            x, y, z, radius, red, green, blue = 0, 0, 0, 0, 0, 0, 0

            print(f"\nInputs for sphere {i + 1}:")

            if DEFAULT_SPHERES.get(i) is not None:
                (default_x, default_y, default_z,
                 default_radius, default_red, default_green,
                 default_blue) = DEFAULT_SPHERES.get(i)
                successful_input = False
                while not successful_input:
                    x = input(f"Position x (default: {default_x}): ")
                    y = input(f"Position y (default: {default_y}): ")
                    z = input(f"Position z (default: {default_z}): ")
                    radius = input(f"Radius (default: {default_radius}): ")
                    red = input(f"Red (default: {default_red}): ")
                    green = input(f"Green (default: {default_green}): ")
                    blue = input(f"Blue (default: {default_blue}): ")
                    if x == '':
                        x = default_x
                    if y == '':
                        y = default_y
                    if z == '':
                        z = default_z
                    if radius == '':
                        radius = default_radius
                    if red == '':
                        red = default_red
                    if green == '':
                        green = default_green
                    if blue == '':
                        blue = default_blue
                    try:
                        x = float(x)
                        y = float(y)
                        z = float(z)
                        radius = float(radius)
                        red = int(red)
                        green = int(green)
                        blue = int(blue)
                    except ValueError:
                        print("Only integer are valid for the colors and floats for the rest")
                        continue
                    if red > 255 or red < 0 or green > 255 or green < 0 or blue > 255 or blue < 0:
                        print("Colors can only be between 0 and 255")
                        continue
                    if radius <= 0:
                        print("Radius has to be bigger than 0")
                        continue
                    successful_input = True
            else:
                successful_input = False
                while not successful_input:
                    x = input("Position x: ")
                    y = input("Position y: ")
                    z = input("Position z: ")
                    radius = input("Radius: ")
                    red = input("Red: ")
                    green = input("Green: ")
                    blue = input("Blue: ")
                    try:
                        x = float(x)
                        y = float(y)
                        z = float(z)
                        radius = float(radius)
                        red = int(red)
                        green = int(green)
                        blue = int(blue)
                    except ValueError:
                        print("Only integer are valid for the colors and floats for the rest")
                        continue
                    if red > 255 or red < 0 or green > 255 or green < 0 or blue > 255 or blue < 0:
                        print("Colors can only be between 0 and 255")
                        continue
                    if radius <= 0:
                        print("Radius has to be bigger than 0")
                        continue
                    successful_input = True

            sphere = Sphere(Vector(x, y, z), radius, Materials.NoTexture(Vector(red, green, blue)))
            spheres.append(sphere)

        scene.add(spheres)
        image = scene.render(width, render_depth)
        image.save_image(path, gamma_correction)


def step5(path: str, width: int, height: int, gamma_correction: bool) -> None:
    focal_length, viewport_width, samples_per_pixel, render_depth = 0, 0, 0, 0
    number_images, number_images_per_depth = 0, 0
    max_depth_default = [1, 2, 4, 8, 16]

    successful_input_number_images = False
    while not successful_input_number_images:
        number_images = input("How many images do you want to render with different render depth (default: 5): ")
        if number_images == '':
            number_images = 5
        try:
            number_images = int(number_images)
        except ValueError:
            print("Only an integer is valid")
            continue
        successful_input_number_images = True

    for k in range(number_images):

        successful_input_number_images_per_depth = False
        while not successful_input_number_images_per_depth:
            if k < len(max_depth_default):
                render_depth = input(f"\n\nPlease choose render depth (default: {max_depth_default[k]}): ")
                if render_depth == '':
                    render_depth = max_depth_default[k]
            else:
                render_depth = input(f"Please choose render depth: ")
            number_images_per_depth = input("How many images do you want to render with different antialiasing ("
                                            "default: 1): ")
            if number_images_per_depth == '':
                number_images_per_depth = 1
            try:
                render_depth = int(render_depth)
                number_images_per_depth = int(number_images_per_depth)
            except ValueError:
                print("Only integer are valid")
                continue
            successful_input_number_images_per_depth = True

        for j in range(number_images_per_depth):
            successful_input = False
            while not successful_input:
                samples_per_pixel = input(
                        f"\nHow many rays per pixel (default: 8): ")
                if samples_per_pixel == '':
                    samples_per_pixel = 8
                try:
                    samples_per_pixel = int(samples_per_pixel)
                except ValueError:
                    print("Only an integer is valid")
                    continue
                successful_input = True
            if k != 0 or j != 0:
                path = input(f"Path for rendered image with render depth {render_depth} "
                             f"and antialiasing {samples_per_pixel}: ")

            successful_input = False
            while not successful_input:
                focal_length = input("Focal length (default: 1.0): ")
                if focal_length == '':
                    focal_length = 1
                viewport_width = input("Viewport width (default: 3.555555555555555555555555555556): ")
                if viewport_width == '':
                    viewport_width = 3.555555555555555555555555555556
                try:
                    focal_length = float(focal_length)
                    viewport_width = float(viewport_width)
                except ValueError:
                    print("Only floats are valid")
                    continue
                successful_input = True

            camera = Camera(Vector(0, 0, 0),
                            focal_length,
                            width / height,
                            viewport_width,
                            samples_per_pixel)
            scene = Scene(camera)

            number_spheres = -1
            successful_input = False
            while not successful_input:
                number_spheres = input("Number of spheres to add (default: 5): ")
                if number_spheres == '':
                    number_spheres = 5
                try:
                    number_spheres = int(number_spheres)
                except ValueError:
                    print("Only an integer is valid")
                    continue
                successful_input = True

            spheres = []
            for i in range(number_spheres):
                x, y, z, radius, red, green, blue = 0, 0, 0, 0, 0, 0, 0

                print(f"\nInputs for sphere {i + 1}:")

                if DEFAULT_SPHERES.get(i) is not None:
                    (default_x, default_y, default_z,
                     default_radius, default_red, default_green,
                     default_blue) = DEFAULT_SPHERES.get(i)
                    successful_input = False
                    while not successful_input:
                        x = input(f"Position x (default: {default_x}): ")
                        y = input(f"Position y (default: {default_y}): ")
                        z = input(f"Position z (default: {default_z}): ")
                        radius = input(f"Radius (default: {default_radius}): ")
                        red = input(f"Red (default: {default_red}): ")
                        green = input(f"Green (default: {default_green}): ")
                        blue = input(f"Blue (default: {default_blue}): ")
                        if x == '':
                            x = default_x
                        if y == '':
                            y = default_y
                        if z == '':
                            z = default_z
                        if radius == '':
                            radius = default_radius
                        if red == '':
                            red = default_red
                        if green == '':
                            green = default_green
                        if blue == '':
                            blue = default_blue
                        try:
                            x = float(x)
                            y = float(y)
                            z = float(z)
                            radius = float(radius)
                            red = int(red)
                            green = int(green)
                            blue = int(blue)
                        except ValueError:
                            print("Only integer are valid for the colors and floats for the rest")
                            continue
                        if red > 255 or red < 0 or green > 255 or green < 0 or blue > 255 or blue < 0:
                            print("Colors can only be between 0 and 255")
                            continue
                        if radius <= 0:
                            print("Radius has to be bigger than 0")
                            continue
                        successful_input = True
                else:
                    successful_input = False
                    while not successful_input:
                        x = input("Position x: ")
                        y = input("Position y: ")
                        z = input("Position z: ")
                        radius = input("Radius: ")
                        red = input("Red: ")
                        green = input("Green: ")
                        blue = input("Blue: ")
                        try:
                            x = float(x)
                            y = float(y)
                            z = float(z)
                            radius = float(radius)
                            red = int(red)
                            green = int(green)
                            blue = int(blue)
                        except ValueError:
                            print("Only integer are valid for the colors and floats for the rest")
                            continue
                        if red > 255 or red < 0 or green > 255 or green < 0 or blue > 255 or blue < 0:
                            print("Colors can only be between 0 and 255")
                            continue
                        if radius <= 0:
                            print("Radius has to be bigger than 0")
                            continue
                        successful_input = True

                sphere = Sphere(Vector(x, y, z), radius, Materials.Specular(Vector(red, green, blue)))
                spheres.append(sphere)

            scene.add(spheres)
            image = scene.render(width, render_depth)
            image.save_image(path, gamma_correction)


METHODS = {1: step1, 2: step2, 3: step3, 4: step4, 5: step5}


def main(arguments: list | None = None) -> None:
    if arguments is None:
        arguments = []

    parser = argparse.ArgumentParser("File for executing all possible steps of the program")
    parser.add_argument("-s", "--step", type=int, help="Step to execute", default=-1)
    parser.add_argument("-p", "--path", type=str, help="Path to save rendered image to", default='')
    parser.add_argument("-w", "--width", type=int, help="Width of the rendered image", default=-1)
    parser.add_argument("-he", "--height", type=int, help="Height of the rendered image", default=-1)

    args = parser.parse_args(arguments)

    step_number = args.step
    already_asked = False
    while step_number not in METHODS.keys():
        if already_asked:
            print("Chosen step is not valid")
        else:
            already_asked = True

        step_number = input("Which step do you want to execute: ")
        try:
            step_number = int(step_number)
        except ValueError:
            print("Chosen step is not valid")
            already_asked = False

    path = args.path
    already_asked = False
    while path == '':
        if already_asked:
            print("Chosen path is not valid")
        else:
            already_asked = True

        path = input("Where do you want to save the rendered image to: ")

    step = METHODS.get(step_number, lambda *args, **kwargs: print("Chosen step is invalid"))

    width = args.width
    already_asked = False
    while not width > 0:
        if already_asked:
            print("Chosen width is not valid")
        else:
            already_asked = True

        width = input("Which width should the rendered image have: ")
        try:
            width = int(width)
        except ValueError:
            width = -1
            print("Chosen width is not valid")
            already_asked = False

    height = args.height
    already_asked = False
    while not height > 0:
        if already_asked:
            print("Chosen height is not valid")
        else:
            already_asked = True

        height = input("Which height should the rendered image have: ")
        try:
            height = int(height)
        except ValueError:
            height = -1
            print("Chosen height is not valid")
            already_asked = False

    gamma_correction = input("Should the images get gamma corrected (default: no; yes or y for yes): ")
    if gamma_correction.lower() in ['yes', 'y']:
        gamma_correction = True
    else:
        gamma_correction = False

    print("\nFor recreating images from results, use all default values\n")

    step(path, width, height, gamma_correction)


if __name__ == '__main__':
    main()
