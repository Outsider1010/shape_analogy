from abc import ABC, abstractmethod

class OverflowPrevention(ABC):

    @abstractmethod
    def getOuterRectangles(self, boundingBoxes, specRectangles, make_bi_rectangle):
        raise NotImplementedError
