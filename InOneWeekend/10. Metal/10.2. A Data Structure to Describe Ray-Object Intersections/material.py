from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from color import Color
from ray import Ray

if TYPE_CHECKING:
    from hittable import HitRecord


class Material(ABC):

    @abstractmethod
    def scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool:
        return False
