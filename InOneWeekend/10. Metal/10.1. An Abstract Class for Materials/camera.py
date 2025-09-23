import logging
import math
import random

from color import Color, write_color
from hittable import HitRecord, Hittable
from interval import Interval
from ray import Ray
from vector import Point3, Vector3, random_on_hemisphere, unit_vector


class Camera:

    def __init__(
        self, aspect_ratio: float = 1, image_width: int = 100, samples_per_pixel: int = 10
    ):
        self.aspect_ratio = aspect_ratio  # Ratio of image width over height
        self.image_width = image_width  # Rendered image width in pixel count
        self.samples_per_pixel = samples_per_pixel  # Count of random samples for each pixel

        self.image_height = int(self.image_width / self.aspect_ratio)  # Rendered image height
        self.image_height = max(1, self.image_height)

        # Color scale factor for a sum of pixel samples
        self.pixel_samples_scale = 1 / self.samples_per_pixel

        self.center = Point3(0, 0, 0)  # Camera center

        # Determine the viewport dimensions.
        focal_length = 1
        viewport_height = 2
        viewport_width = viewport_height * self.image_width / self.image_height

        # Calculate the vectors across the horizontal and down the vertical viewport edges.
        viewport_u = Vector3(viewport_width, 0, 0)
        viewport_v = Vector3(0, -viewport_height, 0)

        # Calculate the horizontal and vertical delta vectors from pixel to pixel.
        self.pixel_delta_u = viewport_u / self.image_width  # Offset to pixel to the right
        self.pixel_delta_v = viewport_v / self.image_height  # Offset to pixel below

        # Calculate the location of the upper left pixel.
        viewport_upper_left = (
            self.center - Vector3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2
        )
        # Location of pixel 0, 0
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

    def sample_square(self) -> Vector3:
        '''Returns the vector to a random point in the [-.5,-.5]-[+.5,+.5] unit square.'''
        return Vector3((random.random() - 0.5), (random.random() - 0.5), 0)

    def get_ray(self, i: int, j: int) -> Ray:
        '''
        Construct a camera ray originating from the origin
        and directed at randomly sampled point around the pixel location i,j.
        '''

        offset = self.sample_square()
        pixel_sample = (
            self.pixel00_loc
            + (i + offset.x) * self.pixel_delta_u
            + (j + offset.y) * self.pixel_delta_v
        )

        ray_origin = self.center
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)

    def ray_color(self, r: Ray, world: Hittable) -> Color:
        rec = HitRecord()

        if world.hit(r, Interval(0, math.inf), rec):
            direction = random_on_hemisphere(rec.normal)
            return 0.5 * self.ray_color(Ray(rec.p, direction), world)

        unit_direction = unit_vector(r.direction)
        a = 0.5 * (unit_direction.y + 1)
        return (1 - a) * Color(1, 1, 1) + a * Color(0.5, 0.7, 1)

    def render(self, world: Hittable):
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

        print('P3')
        print(f'{self.image_width} {self.image_height}')
        print('255')

        for j in range(self.image_height):
            logging.info('Scanlines remaining: %d', self.image_height - j)
            for i in range(self.image_width):
                pixel_color = Color(0, 0, 0)
                for _ in range(self.samples_per_pixel):
                    r = self.get_ray(i, j)
                    pixel_color += self.ray_color(r, world)
                write_color(pixel_color * self.pixel_samples_scale)

        logging.info('Done.')
