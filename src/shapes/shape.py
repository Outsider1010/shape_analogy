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

    @abstractmethod
    def isEmpty(self):
        pass

    @staticmethod
    def analogy(shape_a, shape_b, shape_c, birectAnalogy=BiRectangle.analogy):
        shape_list = (shape_a, shape_b, shape_c)

        birectangles = tuple(BiRectangle(shape.getOuterRectangle(),
                                    shape.getInnerRectangle()) for shape in shape_list)

        birectangle_d = birectAnalogy(*birectangles)

        subshapes = tuple(shape_list[i].cutting_in_4(birectangles[i]) for i in range(3))

        results = [birectangle_d.innerRectangle]
        for i in range(4):
            subshape_a: Shape = subshapes[0][i]
            subshape_b: Shape = subshapes[1][i]
            subshape_c: Shape = subshapes[2][i]
            # if one of the shapes is empty, we don't do anything,
            # but we could (although, we won't have rectangles as solutions)
            if not (subshape_a.isEmpty() or subshape_b.isEmpty() or subshape_c.isEmpty()):
                results.extend(Shape.analogy(subshape_a, subshape_b, subshape_c, birectAnalogy))
            elif subshape_a.isEmpty() and subshape_b.isEmpty() and subshape_c.isEmpty():
                continue
            # elif subshape_a.isEmpty() and subshape_b.isEmpty():
            #     results.append(subshape_c)
            # elif subshape_a.isEmpty() and subshape_c.isEmpty():
            #     results.append(subshape_b)
        return results




