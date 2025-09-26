import logging
import math
import queue
import random
import threading
import time
from pathlib import Path

from color import Color, write_color
from hittable import HitRecord, Hittable
from interval import Interval
from ray import Ray
from vector import Point3, Vector3, cross, random_in_unit_disk, unit_vector


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
        defocus_angle: float = 0,  # Variation angle of rays through each pixel
        focus_dist: float = 10,  # Distance from camera lookfrom point to plane of perfect focus
    ):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel
        self.max_depth = max_depth
        self.vfov = vfov
        self.lookfrom = lookfrom if lookfrom is not None else Point3()
        self.lookat = lookat if lookat is not None else Point3()
        self.vup = vup if vup is not None else Vector3()
        self.defocus_angle = defocus_angle
        self.focus_dist = focus_dist

        self.image_height = int(self.image_width / self.aspect_ratio)  # Rendered image height
        self.image_height = max(1, self.image_height)

        # Color scale factor for a sum of pixel samples
        self.pixel_samples_scale = 1 / self.samples_per_pixel

        self.center = self.lookfrom  # Camera center

        # Determine the viewport dimensions.
        theta = math.radians(self.vfov)
        h = math.tan(theta / 2)
        viewport_height = 2 * h * self.focus_dist
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
            self.center - (self.focus_dist * self.w) - viewport_u / 2 - viewport_v / 2
        )
        # Location of pixel 0, 0
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

        # Calculate the camera defocus disk basis vectors.
        defocus_radius = self.focus_dist * math.tan(math.radians(self.defocus_angle / 2))
        self.defocus_disk_u = self.u * defocus_radius  # Defocus disk horizontal radius
        self.defocus_disk_v = self.v * defocus_radius  # Defocus disk vertical radius

    def sample_square(self) -> Vector3:
        '''Returns the vector to a random point in the [-.5,-.5]-[+.5,+.5] unit square.'''
        return Vector3((random.random() - 0.5), (random.random() - 0.5), 0)

    def defocus_disk_sample(self) -> Point3:
        '''Returns a random point in the camera defocus disk.'''
        p = random_in_unit_disk()
        return self.center + p.x * self.defocus_disk_u + p.y * self.defocus_disk_v

    def get_ray(self, i: int, j: int) -> Ray:
        '''
        Construct a camera ray originating from the defocus disk and
        directed at a randomly sampled point around the pixel location i, j.
        '''

        offset = self.sample_square()
        pixel_sample = (
            self.pixel00_loc
            + (i + offset.x) * self.pixel_delta_u
            + (j + offset.y) * self.pixel_delta_v
        )

        ray_origin = self.center if self.defocus_angle <= 0 else self.defocus_disk_sample()
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

    def render_pixel(self, i: int, j: int, world: Hittable) -> Color:
        pixel_color = Color(0, 0, 0)
        for _ in range(self.samples_per_pixel):
            r = self.get_ray(i, j)
            pixel_color += self.ray_color(r, self.max_depth, world)
        pixel_color *= self.pixel_samples_scale
        return pixel_color

    def log_pixel(self, i: int, j: int):
        if i == 0:
            if j == 0:
                logging.info('Scanlines remaining: %d', self.image_height - j)
            else:
                current_perf_counter_ns = time.perf_counter_ns()
                elapsed_perf_counter_ns = current_perf_counter_ns - self.start_perf_counter_ns
                elapsed_s = elapsed_perf_counter_ns / 1e9
                s_per_line = elapsed_s / j
                total_s = s_per_line * self.image_height
                left_s = total_s - elapsed_s
                logging.info(
                    'Scanlines remaining: %d, %02d:%02d < %02d:%02d < %02d:%02d, %.2fs/line',
                    self.image_height - j,
                    elapsed_s // 60,
                    elapsed_s % 60,
                    left_s // 60,
                    left_s % 60,
                    total_s // 60,
                    total_s % 60,
                    s_per_line,
                )

    def log_done(self):
        current_perf_counter_ns = time.perf_counter_ns()
        total_perf_counter_ns = current_perf_counter_ns - self.start_perf_counter_ns
        total_s = total_perf_counter_ns / 1e9
        logging.info('Done. %02d:%02d', total_s // 60, total_s % 60)

    def render(self, world: Hittable, image_file: Path = Path('image.ppm')):
        f = image_file.open('w')
        f.write(f'P3\n{self.image_width} {self.image_height}\n255\n')

        self.start_perf_counter_ns = time.perf_counter_ns()
        for j in range(self.image_height):
            for i in range(self.image_width):
                self.log_pixel(i, j)
                pixel_color = self.render_pixel(i, j, world)
                write_color(pixel_color, f)

        f.close()
        self.log_done()

    def render_threading(
        self, world: Hittable, image_file: Path = Path('image.ppm'), num_threads: int = 4
    ):
        task_queue: queue.Queue[tuple[int, int]] = queue.Queue()
        result_queue: queue.Queue[tuple[int, int, Color]] = queue.Queue()

        def renderer():
            while True:
                try:
                    j, i = task_queue.get(timeout=1)
                except queue.Empty:
                    break
                self.log_pixel(i, j)
                pixel_color = self.render_pixel(i, j, world)
                result_queue.put((j, i, pixel_color))
                task_queue.task_done()

        for j in range(self.image_height):
            for i in range(self.image_width):
                task_queue.put((j, i))

        threads = [threading.Thread(target=renderer, daemon=True) for _ in range(num_threads)]
        self.start_perf_counter_ns = time.perf_counter_ns()
        for thread in threads:
            thread.start()

        task_queue.join()
        for thread in threads:
            thread.join()

        j_i_pixel_colors = []
        while not result_queue.empty():
            j_i_pixel_colors.append(result_queue.get())
        j_i_pixel_colors.sort()

        with image_file.open('w') as f:
            f.write(f'P3\n{self.image_width} {self.image_height}\n255\n')
            for *_, pixel_color in j_i_pixel_colors:
                write_color(pixel_color, f)

        self.log_done()
