from abc import ABC, abstractmethod
from src.rectangle import Rectangle
from src.birectangle import BiRectangle

class Shape(ABC):

    @abstractmethod
    def getInnerRectangle(self) -> Rectangle:
        pass

    @abstractmethod
    def getOuterRectangle(self) -> Rectangle:
        pass

    @abstractmethod
    def cutting_in_4(self, birectangle: list[Rectangle]):
        pass

    @staticmethod
    @abstractmethod
    def rectangles_to_shape(rectangles):
        pass

    @staticmethod
    def analogy(shape_a, shape_b, shape_c):
        shape_list = (shape_a, shape_b, shape_c)

        birectangles = tuple(BiRectangle(shape.getOutterRectangle(),
                                    shape.getInnerRectangle()) for shape in shape_list)

        birectangle_d = BiRectangle.analogy(*birectangles)

        subshapes = tuple(shape_list[i].cutting_in_4(birectangles[i]) for i in range(3))

        # pour l'instant résultat = liste de rectangles à plot
        results = [birectangle_d.innerRectangle]
        for i in range(4):
            results.extend(Shape.analogy(subshapes[0][i], subshapes[1][i], subshapes[2][i]))

        return Shape.rectangles_to_shape(results)




