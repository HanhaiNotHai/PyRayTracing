import logging
import math

from color import Color, write_color
from hittable import HitRecord, Hittable
from hittable_list import HittableList
from ray import Ray
from sphere import Sphere
from vector import Point3, Vector3


def ray_color(r: Ray, world: Hittable) -> Color:
    rec = HitRecord()
    if world.hit(r, 0, math.inf, rec):
        return 0.5 * (rec.normal + Color(1, 1, 1))

    unit_direction = r.direction.unit_vector()
    a = 0.5 * (unit_direction.y + 1)
    return (1 - a) * Color(1, 1, 1) + a * Color(0.5, 0.7, 1)


def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    # Image

    aspect_ratio = 16 / 9
    image_width = 400

    # Calculate the image height, and ensure it's at least 1.
    image_height = int(image_width / aspect_ratio)
    image_height = max(1, image_height)

    # World

    world = HittableList()

    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -1), 100))

    # Camera

    focal_length = 1
    viewport_height = 2
    viewport_width = viewport_height * image_width / image_height
    camera_center = Point3(0, 0, 0)

    # Calculate the vectors across the horizontal and down the vertical viewport edges.
    viewport_u = Vector3(viewport_width, 0, 0)
    viewport_v = Vector3(0, -viewport_height, 0)

    # Calculate the hotizontal and vertical delta vectors from pixel to pixel.
    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    # Calculate the location of the upper left pixel.
    viewport_upper_left = (
        camera_center - Vector3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2
    )
    pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

    # Render

    print('P3')
    print(f'{image_width} {image_height}')
    print('255')

    for j in range(image_height):
        logging.info('Scanlines remaining: %d', image_height - j)
        for i in range(image_width):
            pixel_center = pixel00_loc + i * pixel_delta_u + j * pixel_delta_v
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)

            pixel_color = ray_color(r, world)
            write_color(pixel_color)

    logging.info('Done.')


if __name__ == '__main__':
    main()
