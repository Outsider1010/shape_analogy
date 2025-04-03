from src.birectangle.overflowprevention.overflow_prevention import OverflowPrevention


class DirectPrevention(OverflowPrevention):

    def getOuterRectangles(self, boundingBoxes, specRectangles, make_bi_rectangle):
        return specRectangles