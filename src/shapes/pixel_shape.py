from math import ceil, floor

import numpy as np
from PIL import Image

import src.shapes.union_rectangles as ur
from src.birectangle.rectangle import Rectangle
from ..birectangle.point import Point

# DO NOT IMPORT STRATEGIES (to avoid circular imports)

# defines how we represent too small (< 1) rectangles
# True -> We color the pixel only if it is at least more than half
# False -> Every pixel containing a potential point of the shape is colored
STRICTNESS = 1


def col_round(x):
    frac = x - floor(x)
    if frac < 0.5: return floor(x)
    return ceil(x)


def coordRangeToMatrixIndexes(arr: np.ndarray, x_min: float, x_max: float,
                              y_min: float, y_max: float, strictness=STRICTNESS) -> tuple[int, int, int, int]:
    h, w = arr.shape
    mi_w = w / 2
    mi_h = h / 2
    if strictness == 0:
        return int(x_min + mi_w), ceil(x_max + mi_w), int(mi_h - y_max), ceil(mi_h - y_min)
    elif strictness == 1:
        return col_round(x_min + mi_w), col_round(x_max + mi_w), col_round(mi_h - y_max), col_round(mi_h - y_min)
    else:
        return ceil(x_min + mi_w), int(x_max + mi_w), ceil(mi_h - y_max), int(mi_h - y_min)


def setRangeValue(arr: np.ndarray, value: np.ndarray | int,
                  x_min: float, x_max: float, y_min: float, y_max: float, strictness=STRICTNESS) -> None:
    x1, x2, y1, y2 = coordRangeToMatrixIndexes(arr, x_min, x_max, y_min, y_max)
    if isinstance(value, int):
        arr[y1:y2, x1:x2] = value
    else:
        x3, x4, y3, y4 = coordRangeToMatrixIndexes(value, x_min, x_max, y_min, y_max, strictness)
        arr[y1:y2, x1:x2] = np.minimum(arr[y1:y2, x1:x2], value[y3:y4, x3:x4])


class PixelShape:
    """
    Representation of shapes using a boolean matrix with even dimensions.
    Each pixel is a square of length 1 and equals True if it is included in the shape
    """

    def __init__(self, array=None, img=None):
        assert (array is not None) or (img is not None), \
            "One of the parameters (array, img) must be set"
        if img is not None:
            array = np.array(Image.open(img))

        self.pixels = array

    def toRectangles(self, lir):
        r = lir.findInnerRectanglePixels(self)
        res = ur.UnionRectangles()
        p = np.copy(self.pixels)
        while r.area() > 1:
            res.addRectangle(r)
            setRangeValue(self.pixels, 255, r.x_min, r.x_max, r.y_min, r.y_max)
            r = lir.findInnerRectanglePixels(self)
        w, h = self.pixels.shape
        positions = np.argwhere(self.pixels == 0)
        for y, x in positions:
            c_y = y - h / 2
            c_x = x - w / 2
            res.addRectangle(Rectangle.fromTopLeft(Point(c_x, c_y), 1, 1))
        self.pixels = p
        return res

    def outer_rectangle(self) -> Rectangle:
        # empty shape
        if self.isEmpty():
            return Rectangle(0, 0, 0, 0)
        h, w = self.pixels.shape
        mat = self.pixels == 0
        ind = np.unravel_index(np.argmax(mat), self.pixels.shape)[0]
        y_max = h / 2 - ind
        temp = np.rot90(mat[ind:])
        ind = np.unravel_index(np.argmax(temp), temp.shape)[0]
        x_max = w / 2 - ind
        temp = np.rot90(temp[ind:])
        ind = np.unravel_index(np.argmax(temp), temp.shape)[0]
        y_min = ind - h / 2
        temp = np.rot90(temp[ind:])
        x_min = np.unravel_index(np.argmax(temp), temp.shape)[0] - w / 2
        return Rectangle(x_min, x_max, y_min, y_max)

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

    def plot(self, ax) -> None:
        h, w = self.dim()
        mat_to_plot = self.pixels
        # transparency when not a black pixel
        alpha = np.ones(mat_to_plot.shape)
        alpha[mat_to_plot != 0] = 0
        ax.imshow(mat_to_plot, cmap='gray', vmin=0, vmax=255, alpha=alpha, extent=(- w / 2, w / 2, - h / 2, h / 2))

    def toImage(self, name: str = "default.bmp"):
        if not name.endswith(".bmp"):
            name += ".bmp"
        img = Image.fromarray(self.pixels, 'L')
        img.save('resources/' + name)
