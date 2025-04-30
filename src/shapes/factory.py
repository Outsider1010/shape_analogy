from decimal import Decimal

from src.birectangle.point import Point
from src.birectangle.rectangle import Rectangle
from src.shapes.shape import Shape
from src.shapes.union_rectangles import UnionRectangles


class ShapeFactory:

    @staticmethod
    def rectangleFromCenter(center: Point, w: Decimal | float, h: Decimal | float) -> Shape:
        x = UnionRectangles()
        x.addRectangle(Rectangle.fromCenter(center, w, h))
        return x


    @staticmethod
    def rectangleFromBottomLeft(botLeft: Point, w: Decimal | float, h: Decimal | float) -> Shape:
        x = UnionRectangles()
        x.addRectangle(Rectangle.fromBottomLeft(botLeft, w, h))
        return x