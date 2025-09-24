import logging
import math
import random

from color import Color, write_color
from hittable import HitRecord, Hittable
from interval import Interval
from ray import Ray
from vector import Point3, Vector3, cross, unit_vector


class Camera:

    def __init__(
        self,
        aspect_ratio: float = 1,  # Ratio of image width over height
        image_width: int = 100,  # Rendered image width in pixel count
        samples_per_pixel: int = 10,  # Count of random samples for each pixel
        max_depth: int = 10,  # Maximum number of ray bounces into scene
        vfov: float = 90,  # Vertical view angle (field of view)
        lookfrom: Point3 | None = None,  # Point camera is looking from
        lookat: Point3 | None = None,  # Point camera is looking at
        vup: Vector3 | None = None,  # Camera-relative "up" direction
    ):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel
        self.max_depth = max_depth
        self.vfov = vfov
        self.lookfrom = lookfrom if lookfrom is not None else Point3()
        self.lookat = lookat if lookat is not None else Point3()
        self.vup = vup if vup is not None else Vector3()

        self.image_height = int(self.image_width / self.aspect_ratio)  # Rendered image height
        self.image_height = max(1, self.image_height)

        # Color scale factor for a sum of pixel samples
        self.pixel_samples_scale = 1 / self.samples_per_pixel

        self.center = self.lookfrom  # Camera center

        # Determine the viewport dimensions.
        focal_length = (self.lookfrom - self.lookat).length()
        theta = math.radians(self.vfov)
        h = math.tan(theta / 2)
        viewport_height = 2 * h * focal_length
        viewport_width = viewport_height * self.image_width / self.image_height

        # Calculate the u,v,w unit basis vectors for the camera coordinate frame.
        # Camera frame basis vectors
        self.w = unit_vector(self.lookfrom - self.lookat)
        self.u = unit_vector(cross(self.vup, self.w))
        self.v = cross(self.w, self.u)

        # Calculate the vectors across the horizontal and down the vertical viewport edges.
        viewport_u = viewport_width * self.u  # Vector across viewport horizontal edge
        viewport_v = viewport_height * -self.v  # Vector down viewport vertical edge

        # Calculate the horizontal and vertical delta vectors from pixel to pixel.
        self.pixel_delta_u = viewport_u / self.image_width  # Offset to pixel to the right
        self.pixel_delta_v = viewport_v / self.image_height  # Offset to pixel below

        # Calculate the location of the upper left pixel.
        viewport_upper_left = (
            self.center - (focal_length * self.w) - viewport_u / 2 - viewport_v / 2
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

    def ray_color(self, r: Ray, depth: int, world: Hittable) -> Color:
        # If we've exceeded the ray bounce limit, no more light is gathered.
        if depth <= 0:
            return Color(0, 0, 0)

        rec = HitRecord()

        if world.hit(r, Interval(0.001, math.inf), rec):
            scattered = Ray()
            attenuation = Color()
            if rec.mat.scatter(r, rec, attenuation, scattered):
                return attenuation * self.ray_color(scattered, depth - 1, world)
            return Color(0, 0, 0)

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
                    pixel_color += self.ray_color(r, self.max_depth, world)
                write_color(pixel_color * self.pixel_samples_scale)

        logging.info('Done.')
