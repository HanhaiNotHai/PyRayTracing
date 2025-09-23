from camera import Camera
from hittable_list import HittableList
from sphere import Sphere
from vector import Point3


def main():
    world = HittableList()

    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -1), 100))

    cam = Camera(aspect_ratio=16 / 9, image_width=400, samples_per_pixel=100)

    cam.render(world)


if __name__ == '__main__':
    main()
