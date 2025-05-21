import logging as lgg

import matplotlib.pyplot as plt
import numpy as np
from collections import deque

from src.birectangle.overflowprevention.no_prevention import NoPrevention
from src.birectangle.overflowprevention.overflow_prevention import OverflowPrevention
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
C_INNER_R_BORDER = "#0000ff"
C_INNER_R_FILL = "k"
C_UNSOLVED_R = "#FFA500"


def make_bi_rectangles(outer_rects, inner_rects, epsilon, biRectangleAnalogy):
    birectangles = []
    for i in range(3):
        b = BiRectangle(outer_rects[i], inner_rects[i])
        b.separate(epsilon)
        birectangles.append(b)

    x = biRectangleAnalogy.analogy(birectangles[0], birectangles[1], birectangles[2], outer_rects[3])
    birectangles.append(x)

    return birectangles


class BiRectangleMethod(ShapeAnalogy):

    def __init__(self, biRectAnalogy: BiRectangleAnalogy = BiSegmentAnalogy(), epsilon: float = 0.01,
                 cutMethod: CuttingMethod = CutIn4EqualParts1(), maxDepth: int = 5, nbIterations: int = 1365,
                 innerRectFinder: InnerRectangleFinder = LargestRectangleFinder(),
                 overflowPrevention: OverflowPrevention = NoPrevention(), subSys: str = '', algo: str = 'iter',
                 plot: str | int = 'last', sameAxis: bool = True):
        assert isinstance(biRectAnalogy, BiRectangleAnalogy)
        assert isinstance(cutMethod, CuttingMethod)
        assert isinstance(innerRectFinder, InnerRectangleFinder)
        assert algo in ['iter', 'rec'], (f"The algorithm keyword should be 'iter' if we want to use the iterative"
                                         f" version or 'rec' for the recursive one")
        assert 0 <= epsilon < 0.5, f"Epsilon value ({epsilon}) is too high (should be < 0.5)"
        assert (isinstance(plot, int) and 0 <= plot) or plot in ['step', 'last', 'none'], PLOT_ASSERT
        assert subSys in ['cut', 'super', 'first', '']
        self.biRectangleAnalogy = biRectAnalogy
        self.cuttingMethod = cutMethod
        self.innerRectFinder = innerRectFinder
        self.epsilon = epsilon
        self.maxDepth = maxDepth
        self.initPlot = self.plot = plot
        self.sameAxis = sameAxis
        self.algo = algo
        self.__margin = 5
        self.nbIterations = nbIterations
        self.overflowPrevention = overflowPrevention
        self.subSys = subSys

    def analogy(self, SA: Shape | PixelShape, SB: Shape | PixelShape, SC: Shape | PixelShape) -> Shape | None:
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
        return self.__analogy_rec_aux(SA, SB, SC, 0, [None] * 4)[0]

    def __analogy_rec_aux(self, SA: Shape, SB: Shape, SC: Shape, k: int,
                  csRectangles: list[Rectangle | None]) -> tuple[Shape | None, list[Rectangle]]:
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
        if self.plot != 'none' and self.sameAxis:
            for s in shapes:
                R = s.outer_rectangle()
                plt_x_min = min(R.x_min, plt_x_min)
                plt_x_max = max(R.x_max, plt_x_max)
                plt_y_min = min(R.y_min, plt_y_min)
                plt_y_max = max(R.y_max, plt_y_max)

        empty = tuple(s.isEmpty() for s in shapes)
        # solvable equations with empty shapes ø : ø :: c : ? with solution c and ø : b :: ø : ? with solution b
        if shapes[0] == shapes[1]:
            d = shapes[2].equiv(csRectangles[2], csRectangles[3])
        elif shapes[0] == shapes[2]:
            d = shapes[1].equiv(csRectangles[1], csRectangles[3])
        elif any(empty):
            lgg.warning(f"k = {k} / Unsolvable equation with empty shape(s) : {'∅' if empty[0] else 'a'}:"
                        f"{'∅' if empty[1] else 'b'}::{'∅' if empty[2] else 'c'}:?. Analogy unsolved.")
        else:
            try:
                d = UnionRectangles()
                birectangles = self.get_bi_rectangles(shapes, d, csRectangles)

                if k < self.maxDepth:
                    cutRectanglesA, cutRectanglesB, cutRectanglesC, cutRectanglesD = tuple(
                        self.cuttingMethod.cutBiRectangle(biRect) for biRect in birectangles)
                    subshapesA, subshapesB, subshapesC = tuple(
                        self.cuttingMethod.cut(shapes[i], birectangles[i]) for i in range(3))
                    for i in range(self.cuttingMethod.nbSubShapes()):
                        subshapeA = subshapesA[i]
                        subshapeB = subshapesB[i]
                        subshapeC = subshapesC[i]
                        cutRs = (cutRectanglesA[i], cutRectanglesB[i], cutRectanglesC[i], cutRectanglesD[i])
                        outerRs = tuple(b.outerRectangle for b in birectangles)
                        subshapeD, plt_unsolved_rects2 = self.__analogy_rec_aux(subshapeA, subshapeB, subshapeC, k + 1,
                                                               self.sub_coord_system(cutRs, outerRs, outerRs if csRectangles[0] is None and self.subSys == 'first' else csRectangles))

                        # if self.plot equals none, then no reason to store rectangles (no plot will be made)
                        if self.plot != 'none':
                            plt_unsolved_rects.extend(plt_unsolved_rects2)
                        # we solved the sub analogy
                        if subshapeD is not None:
                            d += subshapeD
                        elif self.plot != 'none':
                            plt_unsolved_rects.append(cutRectanglesD[i])

                if self.__plotting(k):
                    for i in range(4):
                        # plot bi-rectangles and cutting lines of A, B, C and D
                        plt.figure(chr(ord("A") + i))
                        if self.sameAxis:
                            plt_x_min = min(plt_x_min, birectangles[i].outerRectangle.x_min)
                            plt_x_max = max(plt_x_max, birectangles[i].outerRectangle.x_max)
                            plt_y_min = min(plt_y_min, birectangles[i].outerRectangle.y_min)
                            plt_y_max = max(plt_y_max, birectangles[i].outerRectangle.y_max)
                        birectangles[i].outerRectangle.plotBorder(plt, C_OUTER_R)
                        birectangles[i].innerRectangle.plotBorder(plt, C_INNER_R_BORDER)
                        self.cuttingMethod.plotCuttingLines(plt, birectangles[i])
                    for r in plt_unsolved_rects:
                        plt_x_min = min(plt_x_min, r.x_min)
                        plt_x_max = max(plt_x_max, r.x_max)
                        plt_y_min = min(plt_y_min, r.y_min)
                        plt_y_max = max(plt_y_max, r.y_max)
                        r.plotFilled(plt, C_UNSOLVED_R, zorder=1)
            except (AssertionError, ValueError) as e:
                lgg.warning(f"k = {k} / {e}. Analogy unsolved.")

        if self.__plotting(k):
            self.__set_keys_and_text(plt.figure('D'), f'depth = {k}' if d is not None else '')
            if d is not None:
                d.plot(plt)
                plt_outer_d = d.outer_rectangle()
                plt_x_min = min(plt_x_min, plt_outer_d.x_min)
                plt_x_max = max(plt_x_max, plt_outer_d.x_max)
                plt_y_min = min(plt_y_min, plt_outer_d.y_min)
                plt_y_max = max(plt_y_max, plt_outer_d.y_max)
                plt.axis('square')
                plt.axis((plt_x_min - self.__margin, plt_x_max + self.__margin,
                          plt_y_min - self.__margin, plt_y_max + self.__margin))
            for i in range(3):
                self.__set_keys_and_text(plt.figure(chr(ord("A") + i)), f'depth = {k}')
                shapes[i].plot(plt)
                plt.axis('square')
                if self.sameAxis:
                    plt.axis((plt_x_min - self.__margin, plt_x_max + self.__margin,
                              plt_y_min - self.__margin, plt_y_max + self.__margin))
                else:
                    R = shapes[i].outer_rectangle()
                    plt.axis((R.x_min - self.__margin, R.x_max + self.__margin,
                              R.y_min - self.__margin, R.y_max + self.__margin))
            plt.show()
        return d, plt_unsolved_rects


    def analogy_iter(self, SA: Shape, SB: Shape, SC: Shape) -> None | tuple[UnionRectangles]:
        init_shapes = (SA, SB, SC)
        shapes = (SA, SB, SC)
        d = UnionRectangles()
        # list of rectangles where we could not solve the analogy
        plt_unsolved_rects = []
        plt_x_min = plt_y_min = np.inf
        plt_x_max = plt_y_max = -np.inf
        if self.plot != 'none' and self.sameAxis:
            for s in shapes:
                R = s.outer_rectangle()
                plt_x_min = min(R.x_min, plt_x_min)
                plt_x_max = max(R.x_max, plt_x_max)
                plt_y_min = min(R.y_min, plt_y_min)
                plt_y_max = max(R.y_max, plt_y_max)
        k = 0
        equations = deque()
        equations.append((shapes, [None] * 4, None))
        first = True
        go = k < self.nbIterations and len(equations) != 0
        while go:
            # super rectangles are the outer rectangles of the super-shapes
            # cut rectangles are the rectangles obtained by cutting
            shapes, csRectangles, cutD = equations.popleft()

            empty = tuple(s.isEmpty() for s in shapes)
            if shapes[0] == shapes[1]:
                d += shapes[2].equiv(csRectangles[2] , csRectangles[3])
            elif shapes[0] == shapes[2]:
                d += shapes[1].equiv(csRectangles[1], csRectangles[3])
            elif any(empty):
                lgg.warning(f"k = {k} / Unsolvable equation with empty shape(s) : {'∅' if empty[0] else 'a'}:{'∅' if empty[1] else 'b'}::{'∅' if empty[2] else 'c'}:?. Analogy unsolved.")
                if not first and self.plot != 'none':
                    plt_unsolved_rects.append(cutD)
                elif first:
                    d = None
            else:
                try:
                    birectangles = self.get_bi_rectangles(shapes, d, csRectangles)

                    cutRectanglesA, cutRectanglesB, cutRectanglesC, cutRectanglesD = tuple(
                        self.cuttingMethod.cutBiRectangle(biRect) for biRect in birectangles)
                    subshapesA, subshapesB, subshapesC = tuple(self.cuttingMethod.cut(shapes[i], birectangles[i])
                                                               for i in range(3))
                    nbSubShapes = self.cuttingMethod.nbSubShapes()
                    for i in range(nbSubShapes):
                        cutRs = (cutRectanglesA[i], cutRectanglesB[i], cutRectanglesC[i], cutRectanglesD[i])
                        outerRs = tuple(b.outerRectangle for b in birectangles)
                        equations.append(((subshapesA[i], subshapesB[i], subshapesC[i]),
                                          self.sub_coord_system(cutRs, outerRs, outerRs if csRectangles[0] is None and self.subSys == 'first' else csRectangles), cutRectanglesD[i]))

                    if self.__plotting_iter(True, k):
                        for i in range(4):
                            plt.figure(chr(ord("A") + i))
                            if self.sameAxis:
                                plt_x_min = min(plt_x_min, birectangles[i].outerRectangle.x_min)
                                plt_x_max = max(plt_x_max, birectangles[i].outerRectangle.x_max)
                                plt_y_min = min(plt_y_min, birectangles[i].outerRectangle.y_min)
                                plt_y_max = max(plt_y_max, birectangles[i].outerRectangle.y_max)
                            birectangles[i].outerRectangle.plotBorder(plt, C_OUTER_R)
                            birectangles[i].innerRectangle.plotBorder(plt, C_INNER_R_BORDER)
                            self.cuttingMethod.plotCuttingLines(plt, birectangles[i])

                except AssertionError as e:
                    lgg.warning(f"k = {k} / {e}. Analogy unsolved.")
                    if not first and self.plot != 'none':
                        plt_unsolved_rects.append(cutD)
                    elif first:
                        d = None

            k += 1
            first = False
            go = k < self.nbIterations and len(equations) != 0
            if self.__plotting_iter(go, k):
                plt.figure('D')
                if d is not None:
                    self.__set_keys_and_text(plt.figure('D'), f'iteration {k - 1}')
                    d.plot(plt)
                    x_min, x_max, y_min, y_max = d.outer_rectangle()
                    for r in plt_unsolved_rects:
                        x_min, x_max, y_min, y_max = (min(x_min, r.x_min), max(x_max, r.x_max),
                                                      min(y_min, r.y_min), max(y_max, r.y_max))
                        r.plotFilled(plt, C_UNSOLVED_R, zorder=1)
                    plt_x_min = min(plt_x_min, x_min)
                    plt_x_max = max(plt_x_max, x_max)
                    plt_y_min = min(plt_y_min, y_min)
                    plt_y_max = max(plt_y_max, y_max)
                    plt.axis('square')
                    plt.axis((plt_x_min - self.__margin, plt_x_max + self.__margin,
                              plt_y_min - self.__margin, plt_y_max + self.__margin))

                for i in range(3):
                    self.__set_keys_and_text(plt.figure(chr(ord("A") + i)), f'iteration {k - 1}')
                    init_shapes[i].plot(plt)
                    plt.axis('square')
                    if self.sameAxis:
                        plt.axis((plt_x_min - self.__margin, plt_x_max + self.__margin,
                                  plt_y_min - self.__margin, plt_y_max + self.__margin))
                    else:
                        R = init_shapes[i].outer_rectangle()
                        plt.axis((R.x_min - self.__margin, R.x_max + self.__margin,
                                  R.y_min - self.__margin, R.y_max + self.__margin))
                plt.show()

        return d

    def get_bi_rectangles(self, shapes, d, cs_rectangles):
        bounding_boxes = (shapes[0].outer_rectangle(), shapes[1].outer_rectangle(), shapes[2].outer_rectangle(), None)
        pseudo_inner_rectangles = tuple(s.getInnerRectangle(self.innerRectFinder) for s in shapes)

        if cs_rectangles[0] is None:
            outer_rectangles = bounding_boxes
        else:
            outer_rectangles = self.overflowPrevention.getOuterRectangles(bounding_boxes, cs_rectangles, make_bi_rectangles)

        pseudo_inner_rectangles = [outer_rectangles[i].intersection(pseudo_inner_rectangles[i]) for i in range(3)]
        if any(r is None for r in pseudo_inner_rectangles):
            raise AssertionError('too small rectangles')
        birectangles = make_bi_rectangles(outer_rectangles, pseudo_inner_rectangles, self.epsilon, self.biRectangleAnalogy)

        d.addRectangle(birectangles[3].innerRectangle)

        return birectangles

    def sub_coord_system(self, cutRectangles, outerRectangles, firstRectangles):
        if self.subSys == 'cut':
            return cutRectangles
        elif self.subSys == 'super':
            return outerRectangles
        else:
            return firstRectangles

    def __plotting(self, k: int) -> bool:
        """
        :param k: current depth
        :return: True if a plot should be shown at the end of the current execution
        """
        return (self.plot == 'step' or (self.plot == 'last' and k == 0)
                or (type(self.plot) == int and k <= int(self.plot)))

    def __plotting_iter(self, go, current_iteration) -> bool:
        """
        :param go
        :return: True if a plot should be shown at the end of the current execution
        """
        return (self.plot == 'step' or (self.plot == 'last' and not go)
                or (type(self.plot) == int and current_iteration > int(self.plot)))

    def __set_keys_and_text(self, fig, text: str) -> None:
        """
        Set key reaction and messages
        :param fig: figure reacting
        :param text: text to print
        :return: Nothing.
        """
        fig.canvas.mpl_connect('key_press_event', self.__on_key_press)
        if text != '':
            plt.title('Press Enter to stop plotting, Space to skip to the last \nand any other key to continue step by step')
            plt.xlabel(text)

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

'''

    def analogy_iter(self, SA: Shape, SB: Shape, SC: Shape) -> None | tuple[UnionRectangles, PixelShape]:
        init_shapes = (SA, SB, SC)
        shapes = (SA, SB, SC)
        d = UnionRectangles()
        plt_unsolved_rects = []
        plt_x_min = plt_y_min = np.inf
        plt_x_max = plt_y_max = -np.inf

        if self.plot != 'none' and self.sameAxis:
            for s in shapes:
                R = s.outer_rectangle()
                plt_x_min = min(R.x_min, plt_x_min)
                plt_x_max = max(R.x_max, plt_x_max)
                plt_y_min = min(R.y_min, plt_y_min)
                plt_y_max = max(R.y_max, plt_y_max)

        k = 0
        equations = deque()
        equations.append((shapes, [None] * 4, None))
        RABC = [[], [], []]
        first = True

        fig, axs = plt.subplots(2, 2, figsize=(10, 10))  # Subplot layout
        ax_dict = {'A': axs[0, 0], 'B': axs[0, 1], 'C': axs[1, 0], 'D': axs[1, 1]}

        go = k < self.nbIterations and len(equations) != 0
        while go:
            for ax in ax_dict.values():
                ax.clear()
            shapes, csRectangles, cutD = equations.popleft()
            empty = tuple(s.isEmpty() for s in shapes)

            if shapes[0] == shapes[1]:
                RABC[0].append(shapes[0])
                RABC[1].append(shapes[1])
                RABC[2].append(shapes[2])
                d += shapes[2].equiv(csRectangles[2], csRectangles[3])
            elif shapes[0] == shapes[2]:
                RABC[0].append(shapes[0])
                RABC[1].append(shapes[1])
                RABC[2].append(shapes[2])
                d += shapes[1].equiv(csRectangles[1], csRectangles[3])
            elif any(empty):
                lgg.warning(f"k = {k} / Unsolvable equation with empty shape(s): "
                            f"{'∅' if empty[0] else 'a'}:{'∅' if empty[1] else 'b'}::{'∅' if empty[2] else 'c'}:?.")
                if not first and self.plot != 'none':
                    plt_unsolved_rects.append(cutD)
                elif first:
                    d = None
            else:
                try:
                    birectangles = self.get_bi_rectangles(shapes, d, csRectangles)
                    for i in range(3):
                        RABC[i].append(birectangles[i].innerRectangle)

                    cuts = [self.cuttingMethod.cutBiRectangle(biRect) for biRect in birectangles]
                    subs = [self.cuttingMethod.cut(shapes[i], birectangles[i]) for i in range(3)]
                    nbSubShapes = self.cuttingMethod.nbSubShapes()

                    for i in range(nbSubShapes):
                        cutRs = tuple(c[i] for c in cuts)
                        outerRs = tuple(b.outerRectangle for b in birectangles)
                        equations.append(((subs[0][i], subs[1][i], subs[2][i]),
                                          self.sub_coord_system(cutRs, outerRs, outerRs if csRectangles[
                                                                                               0] is None and self.subSys == 'first' else csRectangles),
                                          cuts[3][i]))

                    if self.__plotting_iter(True, k):
                        labels = ['A', 'B', 'C', 'D']
                        for i in range(4):
                            ax = ax_dict[labels[i]]
                            birectangles[i].outerRectangle.plotBorder(C_OUTER_R, ax=ax)
                            birectangles[i].innerRectangle.plotBorder(C_INNER_R_BORDER, ax=ax)
                            self.cuttingMethod.plotCuttingLines(birectangles[i], ax=ax)

                            if self.sameAxis:
                                r = birectangles[i].outerRectangle
                                plt_x_min = min(plt_x_min, r.x_min)
                                plt_x_max = max(plt_x_max, r.x_max)
                                plt_y_min = min(plt_y_min, r.y_min)
                                plt_y_max = max(plt_y_max, r.y_max)

                except AssertionError as e:
                    lgg.warning(f"k = {k} / {e}. Analogy unsolved.")
                    if not first and self.plot != 'none':
                        plt_unsolved_rects.append(cutD)
                    elif first:
                        d = None

            k += 1
            first = False
            go = k < self.nbIterations and len(equations) != 0

            if self.__plotting_iter(go, k):
                ax = ax_dict['D']
                if d is not None:
                    self.__set_keys_and_text(ax, f'iteration {k - 1}')
                    d.plot(ax=ax)

                    x_min, x_max, y_min, y_max = d.outer_rectangle()
                    for r in plt_unsolved_rects:
                        x_min, x_max = min(x_min, r.x_min), max(x_max, r.x_max)
                        y_min, y_max = min(y_min, r.y_min), max(y_max, r.y_max)
                        r.plotFilled(C_UNSOLVED_R, zorder=1, ax=ax)

                    plt_x_min = min(plt_x_min, x_min)
                    plt_x_max = max(plt_x_max, x_max)
                    plt_y_min = min(plt_y_min, y_min)
                    plt_y_max = max(plt_y_max, y_max)

                for i, key in enumerate(['A', 'B', 'C']):
                    ax = ax_dict[key]
                    self.__set_keys_and_text(ax, f'iteration {k - 1}')
                    init_shapes[i].plot(ax=ax)
                    for r in RABC[i]:
                        if isinstance(r, Rectangle):
                            r.plotFilled(color='gray', zorder=2, ax=ax)
                        else:
                            r.plot(ax, color='gray')

                for ax in ax_dict.values():
                    ax.set_aspect('equal')
                    ax.set_xlim(plt_x_min - self.__margin, plt_x_max + self.__margin)
                    ax.set_ylim(plt_y_min - self.__margin, plt_y_max + self.__margin)

                plt.tight_layout()
                plt.show()

        return d

    # --- Helper method updates below ---

    def __set_keys_and_text(self, ax, text: str) -> None:
        fig = ax.figure
        fig.canvas.mpl_connect('key_press_event', self.__on_key_press)

    def __on_key_press(self, event) -> None:
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
        # Clearing handled automatically per subplot redraw
        event.canvas.stop_event_loop()
'''