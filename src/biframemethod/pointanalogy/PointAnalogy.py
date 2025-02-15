from abc import ABC, abstractmethod

from src.biframemethod.point import Point


class PointAnalogy(ABC):

    @abstractmethod
    def analogy(self, A: Point, B: Point, C: Point) -> Point:
        pass