import math

from camera import Camera
from color import Color
from hittable_list import HittableList
from material import Lambertian
from sphere import Sphere
from vector import Point3


def main():
    world = HittableList()

    R = math.cos(math.pi / 4)

    material_left = Lambertian(Color(0, 0, 1))
    material_right = Lambertian(Color(1, 0, 0))

    world.add(Sphere(Point3(-R, 0, -1), R, material_left))
    world.add(Sphere(Point3(R, 0, -1), R, material_right))

    cam = Camera(
        aspect_ratio=16 / 9, image_width=400, samples_per_pixel=100, max_depth=50, vfov=90
    )

    cam.render(world)


if __name__ == '__main__':
    main()
