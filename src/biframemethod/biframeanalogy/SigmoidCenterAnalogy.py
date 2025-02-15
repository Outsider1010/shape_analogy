from src.biframemethod.biframeanalogy.BiFrameAnalogy import BiFrameAnalogy
from src.biframemethod.birectangle import BiRectangle
from src.basicanalogies.realnumbers import bounded
from src.biframemethod.frameanalogy.CenterFrameAnalogy import CenterFrameAnalogy
from src.biframemethod.rectangle import Rectangle
from src.biframemethod.point import Point


class SigmoidCenterAnalogy(BiFrameAnalogy):

    # TODO : simplifier la fonction
    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle) -> BiRectangle:
        outerD = CenterFrameAnalogy().analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)

        BRA_inner_center = BRA.innerRectangle.center()
        BRA_outer_topLeft = BRA.outerRectangle.topLeft()
        BRB_inner_center = BRB.innerRectangle.center()
        BRB_outer_topLeft = BRB.outerRectangle.topLeft()
        BRC_inner_center = BRC.innerRectangle.center()
        BRC_outer_topLeft = BRC.outerRectangle.topLeft()
        # Geometrical analogy on the rescaled inner rectangles
        xA_rescale = (BRA_inner_center.x - BRA_outer_topLeft.x) / BRA.outerRectangle.w
        xB_rescale = (BRB_inner_center.x - BRB_outer_topLeft.x) / BRB.outerRectangle.w
        xC_rescale = (BRC_inner_center.x - BRC_outer_topLeft.x) / BRC.outerRectangle.w
        xD_rescale = bounded(xA_rescale, xB_rescale, xC_rescale)
        xD = outerD.x_min + outerD.w * xD_rescale

        yA_rescale = (- BRA_inner_center.y + BRA_outer_topLeft.y) / BRA.outerRectangle.h
        yB_rescale = (- BRB_inner_center.y + BRB_outer_topLeft.y) / BRB.outerRectangle.h
        yC_rescale = (- BRC_inner_center.y + BRC_outer_topLeft.y) / BRC.outerRectangle.h
        yD_rescale = bounded(yA_rescale, yB_rescale, yC_rescale)
        yD = outerD.y_max - outerD.h * yD_rescale

        wA_rescale = BRA.innerRectangle.w / BRA.outerRectangle.w
        wB_rescale = BRB.innerRectangle.w / BRB.outerRectangle.w
        wC_rescale = BRC.innerRectangle.w / BRC.outerRectangle.w

        # if-elif added
        if wA_rescale == wC_rescale == 1:
            wD_rescale = wB_rescale
        elif wA_rescale == wB_rescale == 1:
            wD_rescale = wC_rescale
        else:
            wD_rescale = bounded(wA_rescale, wB_rescale, wC_rescale)
        wD = outerD.w * wD_rescale

        hA_rescale = BRA.innerRectangle.h / BRA.outerRectangle.h
        hB_rescale = BRB.innerRectangle.h / BRB.outerRectangle.h
        hC_rescale = BRC.innerRectangle.h / BRC.outerRectangle.h

        # if-elif added
        if hA_rescale == hC_rescale == 1:
            hD_rescale = hB_rescale
        elif hA_rescale == hB_rescale == 1:
            hD_rescale = hC_rescale
        else:
            hD_rescale = bounded(hA_rescale, hB_rescale, hC_rescale)
        hD = outerD.h * hD_rescale

        innerD = Rectangle.fromCenter(Point(xD, yD), wD, hD)

        return BiRectangle(outerD, innerD)

