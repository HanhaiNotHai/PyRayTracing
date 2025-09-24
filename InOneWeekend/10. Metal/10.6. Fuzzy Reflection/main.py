from camera import Camera
from color import Color
from hittable_list import HittableList
from material import Lambertian, Metal
from sphere import Sphere
from vector import Point3


def main():
    world = HittableList()

    material_ground = Lambertian(Color(0.8, 0.8, 0))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left = Metal(Color(0.8, 0.8, 0.8), 0.3)
    material_right = Metal(Color(0.8, 0.6, 0.2), 1)

    world.add(Sphere(Point3(0, -100.5, -1), 100, material_ground))
    world.add(Sphere(Point3(0, 0, -1.2), 0.5, material_center))
    world.add(Sphere(Point3(-1, 0, -1), 0.5, material_left))
    world.add(Sphere(Point3(1, 0, -1), 0.5, material_right))

    cam = Camera(aspect_ratio=16 / 9, image_width=400, samples_per_pixel=100, max_depth=50)

    cam.render(world)


if __name__ == '__main__':
    main()
