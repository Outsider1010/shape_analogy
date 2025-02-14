from abc import ABC, abstractmethod

from src.point import Point


class PointAnalogy(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def analogy(self, A: Point, B: Point, C: Point) -> Point:
        pass