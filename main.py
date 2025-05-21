from src.basicanalogies.realnumbers import bounded
from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.bi_rectangle_method import BiRectangleMethod
from src.birectangle.birectangleanalogy.bi_segment_analogy import BiSegmentAnalogy
from src.birectangle.birectangleanalogy.ext_sigmoid_analogy import ExtSigmoidAnalogy
from src.birectangle.birectangleanalogy.naive_analogy import NaiveAnalogy
from src.birectangle.cuttingmethod.cut_in_4_equal_parts_1 import CutIn4EqualParts1
from src.birectangle.cuttingmethod.cut_in_8 import CuttingIn8
from src.birectangle.cuttingmethod.horizontal_cut import HorizontalCut
from src.birectangle.cuttingmethod.sides_non_disjoint_cut import SidesNonDisjointCut
from src.birectangle.cuttingmethod.vertical_cut import VerticalCut
from src.birectangle.innerrectanglefinder.barycenter_rectangle_finder import BarycenterRectangleFinder
from src.birectangle.innerrectanglefinder.largest_rectangle_finder import LargestRectangleFinder
from src.birectangle.overflowprevention.direct_prevention import DirectPrevention
from src.birectangle.overflowprevention.indirect_prevention import IndirectPrevention
from src.birectangle.overflowprevention.no_prevention import NoPrevention
from src.birectangle.point import Point
from src.birectangle.rectangle import Rectangle
from src.birectangle.rectangleanalogy.area_analogy import AreaAnalogy
from src.birectangle.rectangleanalogy.center_dim_analogy import CenterDimAnalogy
from src.shapes.pixel_shape import PixelShape
from src.shapes.union_rectangles import UnionRectangles

example_1 = (PixelShape(img='resources/circle/circle_1.bmp'),
             PixelShape(img='resources/donut/donut_3.bmp'),
             PixelShape(img='resources/exact_rhombus.bmp'))

example_2 = (PixelShape(img='resources/ellipse/ellipse_1.bmp'),
             PixelShape(img='resources/ellipse/rotated/ellipse_4_330deg.bmp'),
             PixelShape(img='resources/ellipse/rotated/ellipse_4_330deg.bmp'))

example_3 = (PixelShape(img='resources/circle/circle_4.bmp'),
             PixelShape(img='resources/circle/circle_1.bmp'),
             PixelShape(img='resources/circle/circle_3.bmp'))

example_4 = (PixelShape(img='resources/non_sym_shape_1.bmp'),
             PixelShape(img='resources/non_sym_shape_2.bmp'),
             PixelShape(img='resources/non_sym_shape_3.bmp'))

example_5 = (PixelShape(img='resources/arc/arc_1.bmp'),
             PixelShape(img='resources/arc/arc_2.bmp'),
             PixelShape(img='resources/arc/arc_3.bmp'))

def run(ABC):

    m = BiRectangleMethod(biRectAnalogy=BiSegmentAnalogy(), innerRectFinder=LargestRectangleFinder(),
                          cutMethod=HorizontalCut(), overflowPrevention=DirectPrevention(), maxDepth=6,
                          nbIterations=1500, epsilon=1e-6,subSys='cut', algo='iter', sameAxis=True, plot='step')

    m.analogy(*ABC)

def profile(ABC):
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        run(ABC)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()

if __name__ == "__main__" :
    run(example_3)