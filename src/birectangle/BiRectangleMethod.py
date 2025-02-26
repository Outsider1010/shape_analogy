import logging as lgg

import matplotlib.pyplot as plt
import numpy as np

from src.ShapeAnalogy import ShapeAnalogy
from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.Rectangle import Rectangle
from src.birectangle.birectangleanalogy.BiRectangleAnalogy import BiRectangleAnalogy
from src.birectangle.birectangleanalogy.BiSegmentAnalogy import BiSegmentAnalogy
from src.birectangle.cuttingmethod.CuttingMethod import CuttingMethod
from src.birectangle.cuttingmethod.FirstCuttingIn4Method import FirstCuttingIn4Method
from src.birectangle.innerrectanglefinder.InnerRectangleFinder import InnerRectangleFinder
from src.birectangle.innerrectanglefinder.LargestRectangleFinder import LargestRectangleFinder
from src.shapes.pixelShape import PixelShape
from src.shapes.shape import Shape

PLOT_ASSERT = ("`plot` keyword should be set to `step` to see every step, `last` to see only the final step or `none` "
               "if only the resulting shape is needed. Or an integer greater than `0` to see only steps with a depth"
               "lower than `plot`.")


class BiRectangleMethod(ShapeAnalogy):

    def __init__(self, biRectAnalogy: BiRectangleAnalogy = BiSegmentAnalogy(),
                 cutMethod: CuttingMethod = FirstCuttingIn4Method(),
                 innerRectFinder: InnerRectangleFinder = LargestRectangleFinder(),
                 epsilon: float = 0.1, maxDepth: int = 7, keep = 1, plot: str | int = 'last'):
        assert isinstance(biRectAnalogy, BiRectangleAnalogy)
        assert isinstance(cutMethod, CuttingMethod)
        assert isinstance(innerRectFinder, InnerRectangleFinder)
        assert 0 <= epsilon < 0.5, f"Epsilon value ({epsilon}) is too high (should be < 0.5)"
        assert (isinstance(plot, int) and 0 <= plot) or plot in ['step', 'last', 'none'], PLOT_ASSERT
        assert 0 <= keep <= 3, f"'Keep' ({keep}) value is 0, 1, 2 or 3"
        self.biRectangleAnalogy = biRectAnalogy
        self.cuttingMethod = cutMethod
        self.innerRectFinder = innerRectFinder
        self.epsilon = epsilon
        self.maxDepth = maxDepth
        self.initPlot = plot
        self.plot = plot
        self.__margin = 15
        # TODO : TO DO PROPERLY
        # basically "strategies" to prevent the shape from going outside the outer rectangle
        # 0 : "NullStrategy" we don't do anything different in subshapes
        # 1 : OuterRectangle at depth >= 1 are now the rectangles obtained by cutting (no analogy on outer rectangles)
        # 2 : OuterRectangle at depth >= 1 are still the bounding boxes but the analogy is made inside the super outer rectangle (of lower depth)
        # 3 : OuterRectangle at depth >= 1 are still the bounding boxes but the analogy is made inside the cuts rectangles
        self.keep = keep

    def analogy(self, SA: Shape, SB: Shape, SC: Shape) -> PixelShape | None:
        res, _, _ = self.__analogy(SA, SB, SC, 0, None, None)
        # reset the plot keyword (changes if keys are pressed)
        self.plot = self.initPlot
        return res

    def __analogy(self, SA: Shape, SB: Shape, SC: Shape, k: int,
                  cutRectangles: tuple[Rectangle, Rectangle, Rectangle, Rectangle] | None,
                  superRectangles: tuple[Rectangle, Rectangle, Rectangle, Rectangle] | None) -> tuple[
        PixelShape | None, list[Rectangle], list[Rectangle]]:
        """
        Main analogy function
        :param SA: the shape A (first shape)
        :param SB: the shape B (second shape)
        :param SC: the shape C (third shape)
        :param k: the current depth
        :return: A shape D or None if the analogy could not be solved, two lists of rectangles and a pixelShape
        """
        shapes = (SA, SB, SC)
        d = None
        # list of inner rectangles, we plot these to be more precise
        plt_solved_rects = []
        # list of rectangles where we could not solve the analogy
        plt_unsolved_rects = []

        empty = tuple(s.isEmpty() for s in shapes)
        if k == 0 or self.keep != 1:
            outerRectangles = [s.getOuterRectangle() for s in shapes]
        else:
            outerRectangles = cutRectangles
        # solvable equation with empty shapes ø : ø :: ø : ? with solution ø
        if all(empty):
            d = PixelShape(array=np.zeros((2, 2), dtype=np.bool))
            self.__set_keys_and_text(plt.figure('D'), k)
        # unsolvable equations with empty shapes
        elif any(empty):
            lgg.warning(" Unsolvable equation with empty shape(s). Analogy unsolved.")
        else:
            try:
                birectangles = []
                for i in range(3):
                    b = BiRectangle(outerRectangles[i], shapes[i].getInnerRectangle(self.innerRectFinder))
                    # prevents the inner rectangle from touching the outerRectangle (if epsilon > 0)
                    b.separate(self.epsilon)
                    birectangles.append(b)
                if k == 0 or self.keep == 0:
                    outerRD = None
                elif self.keep == 1:
                    outerRD = outerRectangles[3]
                else:
                    birectangles2 = []
                    for i in range(3):
                        b = BiRectangle(superRectangles[i] if self.keep == 2 else cutRectangles[i], outerRectangles[i])
                        # prevents the inner rectangle from touching the outerRectangle (if epsilon > 0)
                        b.separate(self.epsilon)
                        birectangles2.append(b)
                    # outerRD is the innerRectangle of the resulting birectangle
                    outerRD, _ = self.biRectangleAnalogy.analogy(birectangles2[0], birectangles2[1], birectangles2[2],
                                                                 superRectangles[3] if self.keep == 2 else cutRectangles[3])

                birectangle_d = self.biRectangleAnalogy.analogy(birectangles[0], birectangles[1], birectangles[2], outerRD)
                birectangles.append(birectangle_d)
                innerRD, outerRD = birectangle_d
                d = PixelShape(rect=innerRD)
                if len(outerRectangles) == 3:
                    outerRectangles.append(outerRD)

                if k <= self.maxDepth:
                    subRectanglesA, subRectanglesB, subRectanglesC, subRectanglesD = tuple(
                        self.cuttingMethod.cutBiRectangle(biRect) for biRect in birectangles)
                    subshapesA, subshapesB, subshapesC = tuple(
                        shapes[i].cut(birectangles[i], self.cuttingMethod) for i in range(3))
                    nbSubShapes = self.cuttingMethod.nbSubShapes()
                    for i in range(nbSubShapes):
                        subshapeA = subshapesA[i]
                        subshapeB = subshapesB[i]
                        subshapeC = subshapesC[i]
                        #  (prevent useless executions cause cutting a pixel gives the same pixel if strictness = 0)
                        if subshapeA == shapes[0] and subshapeB == shapes[1] and subshapeC == shapes[2]:
                            continue
                        (subshapeD, plt_solved_rects2,
                         plt_unsolved_rects2) = self.__analogy(subshapeA, subshapeB, subshapeC, k + 1,
                                                  (subRectanglesA[i], subRectanglesB[i],
                                                                subRectanglesC[i], subRectanglesD[i]), outerRectangles)
                        # if self.plot equals none, then no reason to store rectangles (no plot will be made)
                        if self.plot != 'none':
                            # TODO : use linked list to improve 'extend' complexity to O(1)
                            plt_solved_rects.extend(plt_solved_rects2)
                            plt_unsolved_rects.extend(plt_unsolved_rects2)
                        # we solved the sub analogy
                        if subshapeD is not None:
                            d += subshapeD
                        elif self.plot != 'none':
                            plt_unsolved_rects.append(subRectanglesD[i])

                if self.plot != 'none':
                    plt_solved_rects.append(innerRD)
                if self.__plotting(k):
                    plt_outerD = outerRD.x_min, outerRD.x_max, outerRD.y_min, outerRD.y_max
                    for i in range(4):
                        # plot bi-rectangles and cutting lines of A, B, C and D
                        plt.figure(chr(ord("A") + i))
                        birectangles[i].outerRectangle.plotBorder("r")
                        birectangles[i].innerRectangle.plotBorder("b")
                        self.cuttingMethod.plotCuttingLines(birectangles[i])
                    for r in plt_solved_rects:
                        plt_outerD = (min(plt_outerD[0], r.x_min), max(plt_outerD[1], r.x_max),
                                      min(plt_outerD[2], r.y_min), max(plt_outerD[3], r.y_max))
                        r.plotFilled("k", zorder=2)
                    for r in plt_unsolved_rects:
                        plt_outerD = (min(plt_outerD[0], r.x_min), max(plt_outerD[1], r.x_max),
                                      min(plt_outerD[2], r.y_min), max(plt_outerD[3], r.y_max))
                        r.plotFilled("#FFA500", zorder=1)
                    self.__set_keys_and_text(plt.figure('D'), k)
                    plt.axis('square')
                    plt.axis((plt_outerD[0] - self.__margin, plt_outerD[1] + self.__margin,
                              plt_outerD[2] - self.__margin, plt_outerD[3] + self.__margin))
            except AssertionError as e:
                lgg.warning(f" {e}. Analogy unsolved.")

        if self.__plotting(k):
            if d is None:
                plt.figure("D").canvas.mpl_connect('key_press_event', self.__on_key_press)
            for i in range(3):
                self.__set_keys_and_text(plt.figure(chr(ord("A") + i)), k)
                shapes[i].plot()
                plt.axis('square')
                plt.axis((outerRectangles[i].x_min - self.__margin, outerRectangles[i].x_max + self.__margin,
                          outerRectangles[i].y_min - self.__margin, outerRectangles[i].y_max + self.__margin))
            plt.show()
        return d, plt_solved_rects, plt_unsolved_rects

    def __plotting(self, k: int) -> bool:
        """
        :param k: current depth
        :return: True if a plot should be shown at the end of the current execution
        """
        return (self.plot == 'step' or (self.plot == 'last' and k == 0)
                or (type(self.plot) == int and k <= int(self.plot)))

    def __set_keys_and_text(self, fig, k: int) -> None:
        """
        Set key reaction and messages
        :param fig: figure reacting
        :param k: the current depth (for text purposes)
        :return: Nothing.
        """
        fig.canvas.mpl_connect('key_press_event', self.__on_key_press)
        plt.title('Press Enter to stop plotting, Space to skip to the end \nand any other key to continue step by step')
        plt.xlabel(f"depth = {k}")

    def __on_key_press(self, event) -> None:
        """
        Manage key presses when showing plots
        :param event: event giving access to the pressed key
        :return: Nothing.
        """
        if event.key == 'shift':
            return
        if event.key == 'enter':
            self.plot = 'none'
            plt.close('all')
            return
        if event.key == ' ':
            self.plot = 'last'
        if event.key in "0123456789":
            self.plot = int(event.key)
        # simply clear but keeps the windows open
        for x in ('A', 'B', 'C', 'D'):
            fig = plt.figure(x)
            fig.clear()
            fig.canvas.stop_event_loop()

    def setBiRectangleAnalogy(self, biRectAnalogy: BiRectangleAnalogy) -> None:
        assert isinstance(biRectAnalogy, BiRectangleAnalogy)
        self.biRectangleAnalogy = biRectAnalogy

    def setCuttingMethod(self, cut_method: CuttingMethod) -> None:
        assert isinstance(cut_method, CuttingMethod)
        self.cuttingMethod = cut_method

    def setInnerRectangleFinder(self, innerRectFinder: InnerRectangleFinder) -> None:
        assert isinstance(innerRectFinder, InnerRectangleFinder)
        self.innerRectFinder = innerRectFinder

    def setEpsilon(self, epsilon: float) -> None:
        assert epsilon < 0.5, f"Epsilon value ({epsilon}) is too high (should be < 0.5)"
        self.epsilon = epsilon

    def setPlottingBehavior(self, plot: int | str):
        assert (isinstance(plot, int) and 0 <= plot) or plot in ['step', 'last', 'none'], PLOT_ASSERT
        self.plot = plot
        self.initPlot = plot
