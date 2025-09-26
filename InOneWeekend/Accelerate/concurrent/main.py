import logging
import random
import sys
from pathlib import Path

from camera import Camera
from color import Color
from hittable_list import HittableList
from material import Dielectric, Lambertian, Metal
from sphere import Sphere
from vector import Point3, Vector3


def main():
    if len(sys.argv) == 1:
        image_file = Path('image.ppm')
    elif len(sys.argv) == 2:
        image_file = Path(sys.argv[1])
    else:
        print('Help: python main.py image.ppm')
        return

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

    world = HittableList()

    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.random()
            center = Point3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())

            if (center - Point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo = Color.random() * Color.random()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo = Color.random(0.5, 1)
                    fuzz = random.uniform(0.5, 1)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1 = Dielectric(1.5)
    world.add(Sphere(Point3(0, 1, 0), 1, material1))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0)
    world.add(Sphere(Point3(4, 1, 0), 1, material3))

    cam = Camera(
        aspect_ratio=16 / 9,
        image_width=320,
        samples_per_pixel=10,
        max_depth=5,
        vfov=20,
        lookfrom=Point3(13, 2, 3),
        lookat=Point3(0, 0, 0),
        vup=Vector3(0, 1, 0),
        defocus_angle=0.6,
        focus_dist=10,
    )

    cam.render_concurrent(world, image_file, max_workers=8)


if __name__ == '__main__':
    main()
