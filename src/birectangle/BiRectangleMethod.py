import logging as lgg

from matplotlib.pyplot import margins

from src.ShapeAnalogy import ShapeAnalogy
from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.birectangleanalogy.BiRectangleAnalogy import BiRectangleAnalogy
from src.birectangle.birectangleanalogy.ExtSigmoidAnalogy import ExtSigmoidAnalogy
from src.birectangle.cuttingmethod.CuttingMethod import CuttingMethod
from src.birectangle.cuttingmethod.FirstCuttingIn4Method import FirstCuttingIn4Method
from src.birectangle.innerrectanglefinder.InnerRectangleFinder import InnerRectangleFinder
from src.birectangle.innerrectanglefinder.LargestRectangleFinder import LargestRectangleFinder
from src.shapes.pixelShape import PixelShape
from src.shapes.shape import Shape
import matplotlib.pyplot as plt


PLOT_ASSERT = ("`plot` keyword should be set to `step` to see every step, `last` to see only the final step or `none` "
               "if only the resulting shape is needed. Or an integer between `0` and `maxDepth` to see only steps with"
               "a depth lower than `plot`.")

def set_axis_and_show(x_min, x_max, y_min, y_max, showD = False) -> None:
    for x in ('A', 'B', 'C', 'D'):
        # a figure for shape D may not appear (if the equation was not solved)
        if not showD and x == 'D':
            continue
        print(x)
        plt.figure(x)
        plt.axis('square')
        plt.axis((x_min, x_max, y_min, y_max))
    plt.show()


class BiRectangleMethod(ShapeAnalogy):

    def __init__(self, biRectAnalogy = ExtSigmoidAnalogy(), cutMethod = FirstCuttingIn4Method(),
                 innerRectFinder = LargestRectangleFinder(), epsilon = 0.1, maxDepth = 6, plot='last'):
        assert epsilon < 0.5, f"Epsilon value ({epsilon}) is too high (should be < 0.5)"
        assert (type(plot) == int and 0 <= int(plot) <= maxDepth) or plot in ['step', 'last', 'none'], PLOT_ASSERT
        self.biRectangleAnalogy = biRectAnalogy
        self.cuttingMethod = cutMethod
        self.innerRectFinder = innerRectFinder
        self.epsilon = epsilon
        self.maxDepth = maxDepth
        self.initPlot = plot
        self.plot = plot

    def analogy(self, SA : Shape, SB : Shape, SC : Shape) -> PixelShape | None:
        res = self.__analogy(SA, SB, SC, 0)
        self.plot = self.initPlot
        return res

    def __analogy(self, SA : Shape, SB : Shape, SC : Shape, k) -> PixelShape | None:
        """
        Main analogy function
        :param SA: the shape A (first shape)
        :param SB: the shape B (second shape)
        :param SC: the shape C (third shape)
        :param k: the current depth
        :return: A shape D or None if the analogy could not be solved
        """
        shapes = (SA, SB, SC)
        d = None
        empty_ = tuple(s.isEmpty() for s in shapes)
        asPixels = tuple(s.toPixelShape() for s in shapes)
        outerRectangles = [s.getOuterRectangle() for s in shapes]
        try:
            # solving equation ø : ø :: c : ? with solution c (2)
            if empty_[0] and empty_[1]:
                if self.__plotting(k):
                    self.__plot_mat("D", asPixels[2], k)
                d = asPixels[2]
            # solving equation ø : b :: ø : ? with solution b (1)
            elif empty_[0] and empty_[2]:
                if self.__plotting(k):
                    self.__plot_mat("D", asPixels[1], k)
                d = asPixels[1]
            # unsolvable equations with empty shapes
            elif any(empty_):
                lgg.warning(" Unsolvable equation with empty shape(s). Analogy unsolved.")
            else:
                birectangles = []
                for i in range(3):
                    b = BiRectangle(outerRectangles[i], shapes[i].getInnerRectangle(self.innerRectFinder))
                    # prevents the inner rectangle from touching the outerRectangle (if epsilon > 0)
                    b.separate(self.epsilon)
                    birectangles.append(b)
                birectangle_d = self.biRectangleAnalogy.analogy(*birectangles)
                innerRD, outerRD = birectangle_d
                d = PixelShape(rect=innerRD)

                if k < self.maxDepth:
                    subRectangles_d = self.cuttingMethod.cutBiRectangle(birectangle_d)
                    subshapes = tuple(shapes[i].cut(birectangles[i], self.cuttingMethod) for i in range(3))
                    nbSubShapes = self.cuttingMethod.nbSubShapes()
                    for i in range(nbSubShapes):
                        subshapeA: Shape = subshapes[0][i]
                        subshapeB: Shape = subshapes[1][i]
                        subshapeC: Shape = subshapes[2][i]
                        subshapeD = self.__analogy(subshapeA, subshapeB, subshapeC, k + 1)
                        if subshapeD is not None:
                            d = d + subshapeD
                        elif self.__plotting(k):
                            subRectangles_d[i].plotFilled("#f7f7f7", zorder=1)

                if self.__plotting(k):
                    for i in range(3):
                        plt.figure(chr(ord("A") + i))
                        # plot A, B, C bi-rectangles and the cutting lines
                        birectangles[i].outerRectangle.plotBorder("r")
                        birectangles[i].innerRectangle.plotBorder("b")
                        self.cuttingMethod.plotCuttingLines(birectangles[i])
                    # switch to shape D
                    self.__set_keys_and_text(plt.figure("D"), k)
                    outerRD.plotBorder("r")
                    innerRD = birectangle_d.innerRectangle
                    innerRD.plotBorder("b")
                    innerRD.plotFilled("k", zorder=3)
                    self.cuttingMethod.plotCuttingLines(birectangle_d)
                    outerRectangles.append(outerRD)
            # plot A, B and C in case one of the shapes was empty, and we solved it without entering the 'else'
            if self.__plotting(k):
                for i in range(3):
                    self.__plot_mat(chr(ord("A") + i), asPixels[i], k)
        except AssertionError as e:
            lgg.warning(f" {e}. Analogy unsolved.")

        if self.__plotting(k):
            # to have all shapes fully visible with the same scale
            # TODO : improve with one loop
            margin = 5
            plt_x_min = min(r.x_min for r in outerRectangles) - margin
            plt_x_max = max(r.x_max for r in outerRectangles) + margin
            plt_y_min = min(r.y_min for r in outerRectangles) - margin
            plt_y_max = max(r.y_max for r in outerRectangles) + margin
            set_axis_and_show(plt_x_min, plt_x_max, plt_y_min, plt_y_max, showD=d is not None)
        return d

    def __plotting(self, k):
        return self.plot == 'step' or (self.plot == 'last' and k == 0) or (type(self.plot) == int and k <= self.plot)

    def __set_keys_and_text(self, fig, k) -> None:
        """
        Set key reaction and message
        :param fig: figure reacting
        :return: Nothing.
        """
        fig.canvas.mpl_connect('key_press_event', self.__on_key_press)
        plt.title('Press Enter to stop plotting, Space to skip to the end \nand any other key to continue step by step')
        plt.xlabel(f"depth = {k}")

    def __plot_mat(self, fig_num: str, mat: PixelShape, k) -> None:
        """
        Plot a grayscale matrix (used to plot pixelShapes)
        :param fig_num: figure id where to plot
        :param mat: the matrix to plot
        :return: Nothing.
        """
        print(fig_num)
        self.__set_keys_and_text(plt.figure(fig_num), k)
        h, w = mat.dim()
        plt.imshow(mat.grayscale(), cmap='gray', vmin=0, vmax=255, extent=(- w / 2, w / 2, - h / 2, h / 2))

    def __on_key_press(self, event) -> None:
        """
        Manage key presses when showing plots
        :param event: event giving access to the pressed key
        :return: Nothing.
        """
        if event.key == "enter":
            self.plot = "none"
        if event.key == " ":
            self.plot = 'last'
        if event.key in "0123456789":
            self.plot = int(event.key)
        # Close all plot windows and clears everything
        plt.close('all')

    def setBiRectangleAnalogy(self, bra: BiRectangleAnalogy) -> None:
        self.biRectangleAnalogy = bra

    def setCuttingMethod(self, cut_method: CuttingMethod) -> None:
        self.cuttingMethod = cut_method

    def setInnerRectangleFinder(self, irf: InnerRectangleFinder) -> None:
        self.innerRectFinder = irf

    def setEpsilon(self, epsilon) -> None:
        assert epsilon < 0.5, f"Epsilon value ({epsilon}) is too high (should be < 0.5)"
        self.epsilon = epsilon

    def setMaxDepth(self, depth) -> None:
        self.maxDepth = depth

    def setPlottingBehavior(self, plot):
        assert plot in ['step', 'last', 'none'], PLOT_ASSERT
        self.plot = plot
        self.initPlot = plot



