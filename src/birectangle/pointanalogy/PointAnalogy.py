from abc import ABC, abstractmethod

from src.birectangle.Point import Point


class PointAnalogy(ABC):

    @abstractmethod
    def analogy(self, A: Point, B: Point, C: Point) -> Point:
        raise NotImplementedError