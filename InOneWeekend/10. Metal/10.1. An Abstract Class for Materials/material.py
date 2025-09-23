from abc import ABC, abstractmethod

from color import Color
from hittable import HitRecord
from ray import Ray


class Material(ABC):

    @abstractmethod
    def scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool:
        return False
