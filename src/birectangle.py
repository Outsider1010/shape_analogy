from rectangle import Rectangle
from basicanalogies import realnumbers as real_analogies
from point import Point

class BiRectangle:
    def __init__(self, outerRectangle: Rectangle, innerRectangle: Rectangle):
        assert outerRectangle.containsRectangle(
            innerRectangle), "Inner rectangle should be contained by outer rectangle"

        self.innerRectangle = innerRectangle
        self.outerRectangle = outerRectangle

    def __repr__(self):
        return "Outer: " + str(self.outerRectangle) + " Inner: " + str(self.innerRectangle)

    def __str__(self):
        return "Outer: " + str(self.outerRectangle) + "\nInner: " + str(self.innerRectangle)

    # write a version using center instead of topLeft
    @staticmethod
    def analogy(BRA, BRB, BRC):
        outerD = Rectangle.analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)

        BRA_inner_topLeft = BRA.innerRectangle.topLeft()
        BRA_outer_topLeft = BRA.outerRectangle.topLeft()
        BRB_inner_topLeft = BRB.innerRectangle.topLeft()
        BRB_outer_topLeft = BRB.outerRectangle.topLeft()
        BRC_inner_topLeft = BRC.innerRectangle.topLeft()
        BRC_outer_topLeft = BRC.outerRectangle.topLeft()
        # Geometrical analogy on the rescaled inner rectangles
        xA_rescale = (BRA_inner_topLeft.x - BRA_outer_topLeft.x) / BRA.outerRectangle.w
        xB_rescale = (BRB_inner_topLeft.x - BRB_outer_topLeft.x) / BRB.outerRectangle.w
        xC_rescale = (BRC_inner_topLeft.x - BRC_outer_topLeft.x) / BRC.outerRectangle.w
        xD_rescale = real_analogies.bounded(xA_rescale, xB_rescale, xC_rescale)
        xD = outerD.x_min + outerD.w * xD_rescale

        yA_rescale = (- BRA_inner_topLeft.y + BRA_outer_topLeft.y) / BRA.outerRectangle.h
        yB_rescale = (- BRB_inner_topLeft.y + BRB_outer_topLeft.y) / BRB.outerRectangle.h
        yC_rescale = (- BRC_inner_topLeft.y + BRC_outer_topLeft.y) / BRC.outerRectangle.h
        yD_rescale = real_analogies.bounded(yA_rescale, yB_rescale, yC_rescale)
        yD = outerD.y_max - outerD.h * yD_rescale

        wA_rescale = (BRA.innerRectangle.w + BRA_inner_topLeft.x
                      - BRA_outer_topLeft.x) / BRA.outerRectangle.w
        wB_rescale = (BRB.innerRectangle.w + BRB_inner_topLeft.x
                      - BRB_outer_topLeft.x) / BRB.outerRectangle.w
        wC_rescale = (BRC.innerRectangle.w + BRC_inner_topLeft.x
                      - BRC_outer_topLeft.x) / BRC.outerRectangle.w

        # if-elif added
        if wA_rescale == wC_rescale == 1:
            wD_rescale = wB_rescale
        elif wA_rescale == wB_rescale == 1:
            wD_rescale = wC_rescale
        else:
            wD_rescale = real_analogies.bounded(wA_rescale, wB_rescale, wC_rescale)
        wD = outerD.x_min - xD + outerD.w * wD_rescale

        hA_rescale = (BRA.innerRectangle.h - BRA_inner_topLeft.y
                      + BRA_outer_topLeft.y) / BRA.outerRectangle.h
        hB_rescale = (BRB.innerRectangle.h - BRB_inner_topLeft.y
                      + BRB_outer_topLeft.y) / BRB.outerRectangle.h
        hC_rescale = (BRC.innerRectangle.h - BRC_inner_topLeft.y
                      + BRC_outer_topLeft.y) / BRC.outerRectangle.h

        # if-elif added
        if hA_rescale == hC_rescale == 1:
            hD_rescale = hB_rescale
        elif hA_rescale == hB_rescale == 1:
            hD_rescale = hC_rescale
        else:
            hD_rescale = real_analogies.bounded(hA_rescale, hB_rescale, hC_rescale)
        hD = yD - outerD.y_max + outerD.h * hD_rescale

        innerD = Rectangle.fromTopLeft(Point(xD, yD), wD, hD)

        return BiRectangle(outerD, innerD)
