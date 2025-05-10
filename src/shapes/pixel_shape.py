from decimal import Decimal

import numpy as np
from math import ceil, floor

from matplotlib import pyplot as plt
from skimage.transform import radon

from src.birectangle.rectangle import Rectangle
import src.shapes.union_rectangles as ur
from .shape import Shape
from PIL import Image

from ..birectangle.Segment import Segment

# DO NOT IMPORT STRATEGIES (to avoid circular imports)

# defines how we represent too small (< 1) rectangles
# True -> We color the pixel only if it is at least more than half
# False -> Every pixel containing a potential point of the shape is colored
STRICTNESS = 1

def col_round(x):
  frac = x - floor(x)
  if frac < 0.5: return floor(x)
  return ceil(x)

def coordRangeToMatrixIndexes(arr: np.ndarray, x_min: Decimal, x_max: Decimal,
                              y_min: Decimal, y_max: Decimal, strictness = STRICTNESS) -> tuple[int, int, int, int]:
    h, w = arr.shape
    mi_w = Decimal(w / 2)
    mi_h = Decimal(h / 2)
    if strictness == 0:
        return int(x_min + mi_w), ceil(x_max + mi_w), int(mi_h - y_max), ceil(mi_h - y_min)
    elif strictness == 1:
        return col_round(x_min + mi_w), col_round(x_max + mi_w), col_round(mi_h - y_max), col_round(mi_h - y_min)
    else:
        return ceil(x_min + mi_w), int(x_max + mi_w), ceil(mi_h - y_max), int(mi_h - y_min)

def setRangeValue(arr: np.ndarray, value : np.ndarray | int,
                  x_min: Decimal, x_max: Decimal, y_min: Decimal, y_max: Decimal, strictness = STRICTNESS) -> None:
    x1, x2, y1, y2 = coordRangeToMatrixIndexes(arr, x_min, x_max, y_min, y_max)
    if isinstance(value, int):
        arr[y1:y2, x1:x2] = value
    else:
        x3, x4, y3, y4 = coordRangeToMatrixIndexes(value, x_min, x_max, y_min, y_max, strictness)
        arr[y1:y2, x1:x2] = np.minimum(arr[y1:y2, x1:x2], value[y3:y4, x3:x4])


class PixelShape(Shape):
    """
    Representation of shapes using a boolean matrix with even dimensions.
    Each pixel is a square of length 1 and equals True if it is included in the shape
    """

    def __init__(self, array=None, img=None, rect=None):
        assert (array is not None) or (img is not None) or (rect is not None), \
            "One of the parameters (array, img or rect) must be set"
        if img is not None:
            array = np.array(Image.open(img))

        if rect is not None:
            h, w = 2 * ceil(max(abs(rect.y_min), abs(rect.y_max))), 2 * ceil(max(abs(rect.x_min), abs(rect.x_max)))
            array = np.full((h, w), 255, dtype=np.uint8)
            setRangeValue(array, 0, rect.x_min, rect.x_max, rect.y_min, rect.y_max)

        self.pixels = array

    def fromShape(self, r: Rectangle):
        h, w = 2 * ceil(max(abs(r.y_min), abs(r.y_max))), 2 * ceil(max(abs(r.x_min), abs(r.x_max)))
        h = max(h, 2)
        w = max(w, 2)
        array = np.full((h, w), 255, dtype=np.uint8)
        setRangeValue(array, self.pixels, r.x_min, r.x_max, r.y_min, r.y_max)
        return PixelShape(array=array)

    def toRectangles(self, lir):
        r = lir.findInnerRectanglePixels(self)
        res = ur.UnionRectangles()
        p = np.copy(self.pixels)
        while r.area() > 0:
            res.addRectangle(r)
            setRangeValue(self.pixels, 255, r.x_min, r.x_max, r.y_min, r.y_max)
            r = lir.findInnerRectanglePixels(self)
        self.pixels = p
        return res

    def __add__(self, other):
        h1, w1 = self.dim()
        h2, w2 = other.dim()
        array = np.zeros((max(h1, h2), max(w1, w2)), dtype=bool)
        setRangeValue(array, self.pixels, Decimal(- w1 / 2), Decimal(w1 / 2), Decimal(- h1 / 2), Decimal(h1 / 2))
        setRangeValue(array, other.pixels, Decimal(- w2 / 2), Decimal(w2 / 2), Decimal(- h2 / 2), Decimal(h2 / 2))
        return PixelShape(array)

    def outer_rectangle(self) -> Rectangle:
        # empty shape
        if self.isEmpty():
            return Rectangle(0, 0, 0, 0)
        h, w = self.pixels.shape
        mat = self.pixels == 0
        ind = np.unravel_index(np.argmax(mat), self.pixels.shape)[0]
        y_max = Decimal(h / 2 - ind)
        temp = np.rot90(mat[ind:])
        ind = np.unravel_index(np.argmax(temp), temp.shape)[0]
        x_max = Decimal(w / 2 - ind)
        temp = np.rot90(temp[ind:])
        ind = np.unravel_index(np.argmax(temp), temp.shape)[0]
        y_min = Decimal(ind - h / 2)
        temp = np.rot90(temp[ind:])
        x_min = Decimal(np.unravel_index(np.argmax(temp), temp.shape)[0] - w / 2)
        return Rectangle(x_min, x_max, y_min, y_max)

    def isTrue(self, x, y):
        return self.pixels[y, x] == 0

    def getInnerRectangle(self, strategy) -> Rectangle:
        return strategy.findInnerRectanglePixels(self)

    def equiv(self, fromCoordSysR: Rectangle, toCoordSysR: Rectangle):
        raise NotImplementedError

    def isPointInShape(self, x: Decimal | float, y: Decimal | float) -> bool:
        h, w = self.dim()
        x_in_mat = int(x + w / 2)
        y_in_mat = int(h / 2 - y)
        if x_in_mat < 0 or x_in_mat > w or y_in_mat < 0 or y_in_mat > h:
            return False

        # supposes that w and h are even else we would check for example if (x - w / 2) is an integer
        x_is_integer = x.is_integer()
        y_is_integer = y.is_integer()
        # we need to check four pixels if both are integers, two if only one is and one if no one is
        xs_to_check = (x_in_mat - 1, x_in_mat) if x_is_integer else (x_in_mat,)
        ys_to_check = (y_in_mat - 1, y_in_mat) if y_is_integer else (y_in_mat,)

        return any(0 <= x < w and 0 <= y < h and self.isTrue(x, y) for x in xs_to_check for y in ys_to_check)

    def isHorizontalSegmentInShape(self, seg: Segment) -> bool:
        assert seg.A.y == seg.B.y, "Must be a horizontal segment"

        h, w = self.dim()
        mi_h = Decimal(h/2)
        mi_w = Decimal(w/2)
        y = int(mi_h - seg.A.y)
        x_min, x_max = sorted([int(seg.A.x + mi_w), int(seg.B.x + mi_w)])

        if not 0 <= y < h:
            return False

        for x in range(x_min, x_max):
            if not (0 <= x < w):
                continue

            if not self.isPointInShape(Decimal(x), Decimal(y)):
                return False

        return True

    def isVerticalSegmentInShape(self, seg : Segment) -> bool:
        assert seg.A.x == seg.B.x, "Must be a vertical segment"

        h, w = self.dim()
        mi_h = Decimal(h / 2)
        mi_w = Decimal(w / 2)
        x = int(int(seg.A.x + mi_w))
        y_min, y_max = sorted([int(mi_h - seg.A.y), int(mi_h - seg.B.y)])

        if not (0 <= x < w):
            return False

        for y in range(y_min, y_max):
            if not (0 <= y < h):
                continue

            if not self.isPointInShape(Decimal(x), Decimal(y)):
                return False

        return True

    def resize(self, min_w: int = 2, min_h: int = 2):
        assert min_w % 2 == 0, f"Minimum width {min_w} must be even."
        assert min_h % 2 == 0, f"Minimum height {min_h} must be even."
        h, w = self.dim()
        new_w = max(min_w, w)
        new_h = max(min_h, h)
        res = np.full((new_h, new_w), 255, dtype=np.uint8)
        y = (new_h - h) // 2
        x = (new_w - w) // 2
        res[y:y + h, x:x + w] = self.pixels
        return PixelShape(array=res)

    def __eq__(self, other):
        if not isinstance(other, PixelShape):
            return False
        h1, w1 = self.dim()
        h2, w2 = other.dim()
        y1, x1 = np.where(self.pixels)
        y2, x2 = np.where(other.pixels)
        y1 = h1 / 2 - y1
        x1 = x1 - w1 / 2
        y2 = h2 / 2 - y2
        x2 = x2 - w2 / 2
        return y1.shape == y2.shape and x1.shape == x2.shape and np.all(y1 == y2) and np.all(x1 == x2)

    def __repr__(self):
        return str(self.pixels)

    def width(self) -> int:
        return self.pixels.shape[1]

    def height(self) -> int:
        return self.pixels.shape[0]

    def isEmpty(self) -> bool:
        return not np.any(self.pixels == 0)

    def dim(self) -> tuple[int, int]:
        return self.pixels.shape

    def plot(self) -> None:
        h, w = self.dim()
        mat_to_plot = self.pixels
        # transparency when not a black pixel
        alpha = np.ones(mat_to_plot.shape)
        alpha[mat_to_plot != 0] = 0
        plt.imshow(mat_to_plot, cmap='gray', vmin=0, vmax=255, alpha=alpha, extent=(- w / 2, w / 2, - h / 2, h / 2))

    def toImage(self, name: str = "default.bmp"):
        if not name.endswith(".bmp"):
            name += ".bmp"
        img = Image.fromarray(self.pixels, 'L')
        img.save('resources/' + name)
