from decimal import Decimal

from src.birectangle.birectangleanalogy.bi_segment_analogy import BiSegmentAnalogy
from src.birectangle.overflowprevention.overflow_prevention import OverflowPrevention

class IndirectPrevention(OverflowPrevention):

    def __init__(self, epsilon = 0.00001, biRectAnalogy = BiSegmentAnalogy()):
        self.epsilon = Decimal(epsilon)
        self.biRectAnalogy = biRectAnalogy

    def getOuterRectangles(self, boundingBoxes, specRectangles, make_bi_rectangles):
        birectangles = make_bi_rectangles(specRectangles, boundingBoxes, self.epsilon, False, self.biRectAnalogy)
        return [b.innerRectangle for b in birectangles]