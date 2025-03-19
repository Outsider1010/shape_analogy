import logging as lgg
from decimal import Decimal

import matplotlib.pyplot as plt
import numpy as np
from collections import deque

from src.shape_analogy import ShapeAnalogy
from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.rectangle import Rectangle
from src.birectangle.birectangleanalogy.bi_rectangle_analogy import BiRectangleAnalogy
from src.birectangle.birectangleanalogy.bi_segment_analogy import BiSegmentAnalogy
from src.birectangle.cuttingmethod.cutting_method import CuttingMethod
from src.birectangle.cuttingmethod.cut_in_4_equal_parts_1 import CutIn4EqualParts1
from src.birectangle.innerrectanglefinder.inner_rectangle_finder import InnerRectangleFinder
from src.birectangle.innerrectanglefinder.largest_rectangle_finder import LargestRectangleFinder
from src.shapes.union_rectangles import UnionRectangles
from src.shapes.pixel_shape import PixelShape
from src.shapes.shape import Shape

PLOT_ASSERT = ("`plot` keyword should be set to `step` to see every step, `last` to see only the final step or `none` "
               "if only the resulting shape is needed. Or an integer greater than `0` to see only steps with a depth"
               "lower than `plot`.")

C_OUTER_R = "r"
C_INNER_R_BORDER = "#ba55d2"
C_INNER_R_FILL = "k"
C_UNSOLVED_R = "#FFA500"


class BiRectangleMethod(ShapeAnalogy):

    def __init__(self, biRectAnalogy: BiRectangleAnalogy = BiSegmentAnalogy(),
                 cutMethod: CuttingMethod = CutIn4EqualParts1(), maxDepth: int = 5, nbIterations: int = 1365,
                 innerRectFinder: InnerRectangleFinder = LargestRectangleFinder(), epsilon: float = 0.01,
                 keep: int = 0, innerReduction: bool = False, algo: str = 'iter', plot: str | int = 'last'):
        assert isinstance(biRectAnalogy, BiRectangleAnalogy)
        assert isinstance(cutMethod, CuttingMethod)
        assert isinstance(innerRectFinder, InnerRectangleFinder)
        assert algo in ['iter', 'rec'], (f"The algorithm keyword should be 'iter' if we want to use the iterative"
                                         f" version or 'rec' for the recursive one")
        assert 0 <= epsilon < 0.5, f"Epsilon value ({epsilon}) is too high (should be < 0.5)"
        assert (isinstance(plot, int) and 0 <= plot) or plot in ['step', 'last', 'none'], PLOT_ASSERT
        assert 0 <= keep <= 4, f"'Keep' ({keep}) value is 0, 1, 2, 3 or 4"
        self.biRectangleAnalogy = biRectAnalogy
        self.cuttingMethod = cutMethod
        self.innerRectFinder = innerRectFinder
        self.epsilon = Decimal(epsilon)
        self.maxDepth = maxDepth
        self.initPlot = self.plot = plot
        self.algo = algo
        self.__margin = 5
        self.nbIterations = nbIterations
        # TODO : TO DO PROPERLY
        # basically "strategies" to prevent the shape from going outside the outer rectangle
        # 0 : "NullStrategy" we don't do anything different in subshapes
        # 1 : OuterRectangle at depth >= 1 are now the rectangles obtained by cutting (no analogy on outer rectangles)
        # 2 : OuterRectangle at depth >= 1 are still the bounding boxes but the analogy is made inside the super outer rectangle (of lower depth)
        # 3 : OuterRectangle at depth >= 1 are still the bounding boxes but the analogy is made inside the cuts rectangles
        # 4 : OuterRectangle at depth >= 1 are now the super outer rectangles (no analogy on outer rectangles)
        self.keep = keep
        self.innerReduction = innerReduction

    def analogy(self, SA: Shape, SB: Shape, SC: Shape) -> Shape | None:
        l = LargestRectangleFinder()
        if isinstance(SA, PixelShape):
            SA = SA.toRectangles(l)
        if isinstance(SB, PixelShape):
            SB = SB.toRectangles(l)
        if isinstance(SC, PixelShape):
            SC = SC.toRectangles(l)

        if self.algo == 'iter':
            res = self.analogy_iter(SA, SB, SC)
        else:
            res = self.analogy_rec(SA, SB, SC)
        self.plot = self.initPlot

        return res

    def analogy_rec(self, SA: Shape, SB: Shape, SC: Shape) -> Shape | None:
        return self.__analogy_rec_aux(SA, SB, SC, 0, None, None)[0]

    def __analogy_rec_aux(self, SA: Shape, SB: Shape, SC: Shape, k: int,
                  cutRectangles: tuple[Rectangle, Rectangle, Rectangle, Rectangle] | None,
                  superRectangles: tuple[Rectangle, Rectangle, Rectangle, Rectangle] | None) -> tuple[Shape | None, list[Rectangle]]:
        """
        Main analogy function
        :param SA: the shape A (first shape)
        :param SB: the shape B (second shape)
        :param SC: the shape C (third shape)
        :param k: the current depth
        :return: A shape D or None if the analogy could not be solved, a list of rectangles
        """
        shapes = (SA, SB, SC)
        d = None
        # list of rectangles where we could not solve the analogy
        plt_unsolved_rects = []
        plt_x_min = plt_y_min = np.inf
        plt_x_max = plt_y_max = -np.inf
        if self.plot != 'none':
            for s in shapes:
                R = s.getOuterRectangle()
                plt_x_min = min(R.x_min, plt_x_min)
                plt_x_max = max(R.x_max, plt_x_max)
                plt_y_min = min(R.y_min, plt_y_min)
                plt_y_max = max(R.y_max, plt_y_max)
        first = k == 0
        empty = tuple(s.isEmpty() for s in shapes)

        # solvable equations with empty shapes ø : ø :: c : ? with solution c and ø : b :: ø : ? with solution b
        if (empty[0] and empty[1]) or (empty[0] and empty[2]):
            x = 2 if empty[0] and empty[1] else 1
            d = shapes[x].equiv(None if first else superRectangles[x], None if first else superRectangles[3])
        elif any(empty):
            lgg.warning(f"k = {k} / Unsolvable equation with empty shape(s) : {'∅' if empty[0] else 'a'}:"
                        f"{'∅' if empty[1] else 'b'}::{'∅' if empty[2] else 'c'}:?. Analogy unsolved.")
            if not first and self.plot != 'none':
                plt_unsolved_rects.append(cutRectangles[3])
        else:
            try:
                d = UnionRectangles()
                birectangles, outerRectangles = self.getBirectangles(first, shapes, d, cutRectangles, superRectangles)

                if k < self.maxDepth:
                    subRectanglesA, subRectanglesB, subRectanglesC, subRectanglesD = tuple(
                        self.cuttingMethod.cutBiRectangle(biRect) for biRect in birectangles)
                    subshapesA, subshapesB, subshapesC = tuple(
                        self.cuttingMethod.cut(shapes[i], birectangles[i]) for i in range(3))
                    nbSubShapes = self.cuttingMethod.nbSubShapes()
                    for i in range(nbSubShapes):
                        subshapeA = subshapesA[i]
                        subshapeB = subshapesB[i]
                        subshapeC = subshapesC[i]
                        subshapeD, plt_unsolved_rects2 = self.__analogy_rec_aux(subshapeA, subshapeB, subshapeC, k + 1,
                                                               (subRectanglesA[i], subRectanglesB[i],
                                                                subRectanglesC[i], subRectanglesD[i]), outerRectangles)

                        # if self.plot equals none, then no reason to store rectangles (no plot will be made)
                        if self.plot != 'none':
                            plt_unsolved_rects.extend(plt_unsolved_rects2)
                        # we solved the sub analogy
                        if subshapeD is not None:
                            d += subshapeD
                        elif self.plot != 'none':
                            plt_unsolved_rects.append(subRectanglesD[i])

                if self.__plotting(k):
                    for i in range(4):
                        # plot bi-rectangles and cutting lines of A, B, C and D
                        plt.figure(chr(ord("A") + i))
                        birectangles[i].outerRectangle.plotBorder(C_OUTER_R)
                        birectangles[i].innerRectangle.plotBorder(C_INNER_R_BORDER)
                        self.cuttingMethod.plotCuttingLines(birectangles[i])
                    for r in plt_unsolved_rects:
                        plt_x_min = min(plt_x_min, r.x_min)
                        plt_x_max = max(plt_x_max, r.x_max)
                        plt_y_min = min(plt_y_min, r.y_min)
                        plt_y_max = max(plt_y_max, r.y_max)
                        r.plotFilled(C_UNSOLVED_R, zorder=1)
            except AssertionError as e:
                lgg.warning(f" {e}. Analogy unsolved.")

        if self.__plotting(k):
            self.__set_keys_and_text(plt.figure('D'), k, d is not None)
            if d is not None:
                d.plot()
                plt_outer_d = d.getOuterRectangle()
                plt_x_min = min(plt_x_min, plt_outer_d.x_min)
                plt_x_max = max(plt_x_max, plt_outer_d.x_max)
                plt_y_min = min(plt_y_min, plt_outer_d.y_min)
                plt_y_max = max(plt_y_max, plt_outer_d.y_max)
                plt.axis('square')
                plt.axis((plt_x_min - self.__margin, plt_x_max + self.__margin,
                          plt_y_min - self.__margin, plt_y_max + self.__margin))
            for i in range(3):
                self.__set_keys_and_text(plt.figure(chr(ord("A") + i)), k)
                shapes[i].plot()
                plt.axis('square')
                plt.axis((plt_x_min - self.__margin, plt_x_max + self.__margin,
                          plt_y_min - self.__margin, plt_y_max + self.__margin))
            plt.show()
        return d, plt_unsolved_rects


    def analogy_iter(self, SA: Shape, SB: Shape, SC: Shape) -> None | tuple[UnionRectangles, PixelShape]:
        init_shapes = (SA, SB, SC)
        shapes = (SA, SB, SC)
        d = UnionRectangles()
        # list of rectangles where we could not solve the analogy
        plt_unsolved_rects = []
        plt_x_min = plt_y_min = np.inf
        plt_x_max = plt_y_max = -np.inf
        if self.plot != 'none':
            for s in shapes:
                R = s.getOuterRectangle()
                plt_x_min = min(R.x_min, plt_x_min)
                plt_x_max = max(R.x_max, plt_x_max)
                plt_y_min = min(R.y_min, plt_y_min)
                plt_y_max = max(R.y_max, plt_y_max)
        k = 0
        equations = deque()
        equations.append((shapes, [], []))
        first = True
        while k < self.nbIterations and len(equations) != 0:
            # super rectangles are the outer rectangles of the super-shapes
            # cut rectangles are the rectangles obtained by cutting
            shapes, superRectangles, cutRectangles = equations.popleft()

            empty = tuple(s.isEmpty() for s in shapes)
            if (empty[0] and empty[1]) or (empty[0] and empty[2]):
                x = 2 if empty[0] and empty[1] else 1
                d += shapes[x].equiv(None if first else superRectangles[x] , None if first else superRectangles[3])
            elif any(empty):
                lgg.warning(f"k = {k} / Unsolvable equation with empty shape(s) : {'∅' if empty[0] else 'a'}:{'∅' if empty[1] else 'b'}::{'∅' if empty[2] else 'c'}:?. Analogy unsolved.")
                if not first and self.plot != 'none':
                    plt_unsolved_rects.append(cutRectangles[3])
                elif first:
                    d = None
            else:
                try:
                    birectangles, outerRectangles = self.getBirectangles(first, shapes, d, cutRectangles, superRectangles)

                    if first and self.plot != 'none':
                        for i in range(4):
                            plt.figure(chr(ord("A") + i))
                            birectangles[i].outerRectangle.plotBorder(C_OUTER_R)
                            birectangles[i].innerRectangle.plotBorder(C_INNER_R_BORDER)
                            self.cuttingMethod.plotCuttingLines(birectangles[i])

                    cutRectanglesA, cutRectanglesB, cutRectanglesC, cutRectanglesD = tuple(
                        self.cuttingMethod.cutBiRectangle(biRect) for biRect in birectangles)
                    subshapesA, subshapesB, subshapesC = tuple(self.cuttingMethod.cut(shapes[i], birectangles[i])
                                                               for i in range(3))
                    nbSubShapes = self.cuttingMethod.nbSubShapes()
                    for i in range(nbSubShapes):
                        equations.append(((subshapesA[i], subshapesB[i], subshapesC[i]), outerRectangles,
                                          (cutRectanglesA[i], cutRectanglesB[i], cutRectanglesC[i], cutRectanglesD[i])))
                except AssertionError as e:
                    lgg.warning(f"k = {k} / {e}. Analogy unsolved.")
                    if not first and self.plot != 'none':
                        plt_unsolved_rects.append(cutRectangles[3])
                    elif first:
                        d = None
            k += 1
            first = False

        if self.plot != 'none':
            plt.figure('D')
            if d is not None:
                d.plot()
                x_min, x_max, y_min, y_max = d.getOuterRectangle()
                for r in plt_unsolved_rects:
                    x_min, x_max, y_min, y_max = (min(x_min, r.x_min), max(x_max, r.x_max),
                                                  min(y_min, r.y_min), max(y_max, r.y_max))
                    r.plotFilled(C_UNSOLVED_R, zorder=1)
                plt_x_min = min(plt_x_min, x_min)
                plt_x_max = max(plt_x_max, x_max)
                plt_y_min = min(plt_y_min, y_min)
                plt_y_max = max(plt_y_max, y_max)
                plt.axis('square')
                plt.axis((plt_x_min, plt_x_max, plt_y_min, plt_y_max))
            for i in range(3):
                plt.figure(chr(ord("A") + i))
                init_shapes[i].plot()
                plt.axis('square')
                plt.axis((plt_x_min, plt_x_max, plt_y_min, plt_y_max))
            plt.show()
        return d

    def getBirectangles(self, first, shapes, d, cutRectangles, superRectangles):
        if first or (self.keep != 1 and self.keep != 4):
            outerRectangles = [s.getOuterRectangle() for s in shapes]
        elif self.keep == 1:
            outerRectangles = cutRectangles
        else:  # keep == 4
            outerRectangles = superRectangles
        birectangles = []
        r_x_min = r_x_max = r_y_min = r_y_max = Decimal(1)
        for i in range(3):
            b = BiRectangle(outerRectangles[i], shapes[i].getInnerRectangle(self.innerRectFinder))
            birectangles.append(b)
            if self.innerReduction:
                r_x_min = Decimal.min(r_x_min, b.center_x_min_ratio())
                r_x_max = Decimal.min(r_x_max, b.center_x_max_ratio())
                r_y_min = Decimal.min(r_y_min, b.center_y_min_ratio())
                r_y_max = Decimal.min(r_y_max, b.center_y_max_ratio())
        for b in birectangles:
            if self.innerReduction:
                b.reduceInnerTo(r_x_min, r_x_max, r_y_min, r_y_max)
            b.separate(self.epsilon)

        if first or self.keep == 0:
            outerRD = None
        elif self.keep == 1 or self.keep == 4:
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
                                                         superRectangles[3] if self.keep == 2 else
                                                         cutRectangles[3])

        birectangle_d = self.biRectangleAnalogy.analogy(birectangles[0], birectangles[1],
                                                        birectangles[2], outerRD)
        birectangles.append(birectangle_d)
        innerRD, outerRD = birectangle_d
        d.addRectangle(innerRD)
        if len(outerRectangles) == 3:
            outerRectangles.append(outerRD)

        return birectangles, outerRectangles

    def __plotting(self, k: int) -> bool:
        """
        :param k: current depth
        :return: True if a plot should be shown at the end of the current execution
        """
        return (self.plot == 'step' or (self.plot == 'last' and k == 0)
                or (type(self.plot) == int and k <= int(self.plot)))

    def __set_keys_and_text(self, fig, k: int, addText:bool = True) -> None:
        """
        Set key reaction and messages
        :param fig: figure reacting
        :param k: the current depth (for text purposes)
        :return: Nothing.
        """
        fig.canvas.mpl_connect('key_press_event', self.__on_key_press)
        if addText:
            plt.title('Press Enter to stop plotting, Space to skip to the last \nand any other key to continue step by step')
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

    def setEpsilon(self, epsilon: Decimal | float) -> None:
        assert epsilon < 0.5, f"Epsilon value ({epsilon}) is too high (should be < 0.5)"
        self.epsilon = Decimal(epsilon)

    def setPlottingBehavior(self, plot: int | str):
        assert (isinstance(plot, int) and 0 <= plot) or plot in ['step', 'last', 'none'], PLOT_ASSERT
        self.plot = plot
        self.initPlot = plot
