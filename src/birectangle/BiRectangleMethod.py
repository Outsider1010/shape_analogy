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
                 epsilon: float = 0.1, maxDepth: int = 7, plot: str | int = 'last'):
        assert isinstance(biRectAnalogy, BiRectangleAnalogy)
        assert isinstance(cutMethod, CuttingMethod)
        assert isinstance(innerRectFinder, InnerRectangleFinder)
        assert 0 <= epsilon < 0.5, f"Epsilon value ({epsilon}) is too high (should be < 0.5)"
        assert (isinstance(plot, int) and 0 <= plot) or plot in ['step', 'last', 'none'], PLOT_ASSERT
        self.biRectangleAnalogy = biRectAnalogy
        self.cuttingMethod = cutMethod
        self.innerRectFinder = innerRectFinder
        self.epsilon = epsilon
        self.maxDepth = maxDepth
        self.initPlot = plot
        self.plot = plot

    def analogy(self, SA: Shape, SB: Shape, SC: Shape) -> PixelShape | None:
        res, _, _, _ = self.__analogy(SA, SB, SC, 0)
        # reset the plot keyword (changes if keys are pressed)
        self.plot = self.initPlot
        return res

    def __analogy(self, SA: Shape, SB: Shape, SC: Shape,
                  k: int) -> tuple[PixelShape | None, list[Rectangle], list[Rectangle], PixelShape]:
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
        # a pixel shape obtained from executions at higher depths (when solved with empty shape)
        plt_subshape = None
        emptyA, emptyB, emptyC = tuple(s.isEmpty() for s in shapes)
        asPixels = tuple(s.toPixelShape() for s in shapes)
        outerRectangles = [s.getOuterRectangle() for s in shapes]

        # solvable equations with empty shapes
        # ø : ø :: c : ? with solution c (2) or ø : b :: ø : ? with solution b (1)
        if (emptyA and emptyB) or (emptyA and emptyC):
            # 2 = C and 1 = B
            solution = 2 if emptyA and emptyB else 1
            plt_subshape = d = asPixels[solution]
            outerRectangles.append(outerRectangles[solution])
        # unsolvable equations with empty shapes
        elif emptyA or emptyB or emptyC:
            lgg.warning(" Unsolvable equation with empty shape(s). Analogy unsolved.")
        else:
            try:
                birectangles = []
                for i in range(3):
                    b = BiRectangle(outerRectangles[i], shapes[i].getInnerRectangle(self.innerRectFinder))
                    # prevents the inner rectangle from touching the outerRectangle (if epsilon > 0)
                    b.separate(self.epsilon)
                    birectangles.append(b)
                birectangle_d = self.biRectangleAnalogy.analogy(*birectangles)
                birectangles.append(birectangle_d)
                innerRD, outerRD = birectangle_d
                d = PixelShape(rect=innerRD)
                plt_outerD = outerRD.x_min, outerRD.x_max, outerRD.y_min, outerRD.y_max

                if k <= self.maxDepth:
                    subRectangles_d = self.cuttingMethod.cutBiRectangle(birectangle_d)
                    subshapesA, subshapesB, subshapesC = tuple(
                        shapes[i].cut(birectangles[i], self.cuttingMethod) for i in range(3))
                    nbSubShapes = self.cuttingMethod.nbSubShapes()
                    for i in range(nbSubShapes):
                        subshapeA = subshapesA[i]
                        subshapeB = subshapesB[i]
                        subshapeC = subshapesC[i]
                        #  (prevent useless executions cause cutting a pixel gives the same pixel if strictness = 1)
                        if subshapeA == shapes[0] and subshapeB == shapes[1] and subshapeC == shapes[2]:
                            continue
                        (subshapeD, plt_solved_rects2, plt_unsolved_rects2,
                         plt_subshape2) = self.__analogy(subshapeA, subshapeB, subshapeC, k + 1)
                        # if self.plot equals none, then no reason to store rectangles (no plot will be made)
                        if self.plot != 'none':
                            # TODO : use linked list to improve 'extend' complexity to O(1)
                            plt_solved_rects.extend(plt_solved_rects2)
                            plt_unsolved_rects.extend(plt_unsolved_rects2)
                            if plt_subshape is None:
                                plt_subshape = plt_subshape2
                            elif plt_subshape2 is not None:
                                plt_subshape += plt_subshape2
                        # we solved the sub analogy
                        if subshapeD is not None:
                            d += subshapeD
                        elif self.plot != 'none':
                            plt_unsolved_rects.append(subRectangles_d[i])

                if self.plot != 'none':
                    plt_solved_rects.append(innerRD)
                if self.__plotting(k):
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
                outerRectangles.append(Rectangle(*plt_outerD))
            except AssertionError as e:
                lgg.warning(f" {e}. Analogy unsolved.")

        if self.__plotting(k):
            margin = 15
            if d is None:
                # noinspection PyTypeChecker
                plt.figure("D").canvas.mpl_connect('key_press_event', self.__on_key_press)
            for i in range(4 if d is not None else 3):
                self.__setup_fig_with_mat(chr(ord("A") + i), asPixels[i] if i < 3 else plt_subshape, k)
                plt.axis('square')
                plt.axis((outerRectangles[i].x_min - margin, outerRectangles[i].x_max + margin,
                          outerRectangles[i].y_min - margin, outerRectangles[i].y_max + margin))
            plt.show()
        return d, plt_solved_rects, plt_unsolved_rects, plt_subshape

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

    def __setup_fig_with_mat(self, fig_num: str, mat: PixelShape, k: int) -> None:
        """
        Switch to a figure and set up the figure text. Also plot a grayscale matrix if given
        :param fig_num: figure id where to plot
        :param mat: the matrix to plot
        :param k: current depth (for text purposes)
        :return: Nothing.
        """
        self.__set_keys_and_text(plt.figure(fig_num), k)
        if mat:
            h, w = mat.dim()
            mat_to_plot = mat.grayscale()
            # transparency when not a black pixel
            alpha = np.ones(mat_to_plot.shape)
            alpha[mat_to_plot != 0] = 0
            plt.imshow(mat_to_plot, cmap='gray', vmin=0, vmax=255, alpha=alpha, extent=(- w / 2, w / 2, - h / 2, h / 2))

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
        # simply clear but keeps the window
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
