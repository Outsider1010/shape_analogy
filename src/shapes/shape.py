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
    def cutting_in_4(self, birectangle):
        pass

    @staticmethod
    def analogy(shape_a, shape_b, shape_c):
        shape_list = (shape_a, shape_b, shape_c)

        birectangles = tuple(BiRectangle(shape.getOutterRectangle(),
                                    shape.getInnerRectangle()) for shape in shape_list)

        birectangle_d = BiRectangle.analogy(*birectangles)

        subshapes = tuple(shape_list[i].cutting_in_4(birectangles[i]) for i in range(3))

        results = [birectangle_d.innerRectangle]
        for i in range(4):
            subshape_a = subshapes[0][i]
            subshape_b = subshapes[1][i]
            subshape_c = subshapes[2][i]
            # if one of the shapes is empty, we don't do anything,
            # but we should, some equations can be resolved (tho, we won't have rectangles as solutions)
            if not (subshape_a.isblank() or subshape_b.isblank() or subshape_c.isblank()):
                results.extend(Shape.analogy(subshape_a, subshape_b, subshape_c))

        return results




