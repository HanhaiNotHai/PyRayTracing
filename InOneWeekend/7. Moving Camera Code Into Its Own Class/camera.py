import logging
import math

from color import Color, write_color
from hittable import HitRecord, Hittable
from interval import Interval
from ray import Ray
from vector import Point3, Vector3, unit_vector


class Camera:

    def __init__(self, aspect_ratio: float = 1, image_width: int = 100):
        self.aspect_ratio = aspect_ratio  # Ratio of image width over height
        self.image_width = image_width  # Rendered image width in pixel count

        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = max(1, self.image_height)

        self.center = Point3(0, 0, 0)

        # Determine the viewport dimensions.
        focal_length = 1
        viewport_height = 2
        viewport_width = viewport_height * self.image_width / self.image_height

        # Calculate the vectors across the horizontal and down the vertical viewport edges.
        viewport_u = Vector3(viewport_width, 0, 0)
        viewport_v = Vector3(0, -viewport_height, 0)

        # Calculate the hotizontal and vertical delta vectors from pixel to pixel.
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate the location of the upper left pixel.
        viewport_upper_left = (
            self.center - Vector3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2
        )
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

    def ray_color(self, r: Ray, world: Hittable) -> Color:
        rec = HitRecord()

        if world.hit(r, Interval(0, math.inf), rec):
            return 0.5 * (rec.normal + Color(1, 1, 1))

        unit_direction = unit_vector(r.direction)
        a = 0.5 * (unit_direction.y + 1)
        return (1 - a) * Color(1, 1, 1) + a * Color(0.5, 0.7, 1)

    def render(self, world: Hittable):
        print('P3')
        print(f'{self.image_width} {self.image_height}')
        print('255')

        for j in range(self.image_height):
            logging.info('Scanlines remaining: %d', self.image_height - j)
            for i in range(self.image_width):
                pixel_center = self.pixel00_loc + i * self.pixel_delta_u + j * self.pixel_delta_v
                ray_direction = pixel_center - self.center
                r = Ray(self.center, ray_direction)

                pixel_color = self.ray_color(r, world)
                write_color(pixel_color)

        logging.info('Done.')
