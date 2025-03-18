import numpy as np
from math import ceil

from matplotlib import pyplot as plt
from skimage.transform import radon

from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.Rectangle import Rectangle
from .shape import Shape
from PIL import Image
# DO NOT IMPORT STRATEGIES (to avoid circular imports)

# defines how we represent too small (< 1) rectangles
# True -> We color the pixel only if it is at least more than half
# False -> Every pixel containing a potential point of the shape is colored
STRICTNESS = 2

def coordRangeToMatrixIndexes(arr: np.ndarray, x_min: float, x_max: float,
                              y_min: float, y_max: float) -> tuple[float, float, float, float]:
    h, w = arr.shape
    if STRICTNESS == 0:
        return int(x_min + w / 2), ceil(x_max + w / 2), int(h / 2 - y_max), ceil(h / 2 - y_min)
    elif STRICTNESS == 1:
        return round(x_min + w / 2), round(x_max + w / 2), round(h / 2 - y_max), round(h / 2 - y_min)
    else:
        return ceil(x_min + w / 2), int(x_max + w / 2), ceil(h / 2 - y_max), int(h / 2 - y_min)

def setRangeValue(arr: np.ndarray, value : np.ndarray | bool,
                  x_min: float, x_max: float, y_min: float, y_max: float) -> None:
    x1, x2, y1, y2 = coordRangeToMatrixIndexes(arr, x_min, x_max, y_min, y_max)

    if isinstance(value, bool):
        arr[y1:y2, x1:x2] = value
    else:
        x3, x4, y3, y4 = coordRangeToMatrixIndexes(value, x_min, x_max, y_min, y_max)
        arr[y1:y2, x1:x2] |= value[y3:y4, x3:x4]


class PixelShape(Shape):
    """
    Representation of shapes using a boolean matrix with even dimensions.
    Each pixel is a square of length 1 and equals True if it is included in the shape
    """

    def __init__(self, array=None, img=None, rect=None):
        assert (array is not None) or (img is not None) or (rect is not None), \
            "One of the parameters (array, img or rect) must be set"

        if img is not None:
            array = np.array(Image.open(img)) == 0

        if rect is not None:
            h, w = 2 * ceil(max(abs(rect.y_min), abs(rect.y_max))), 2 * ceil(max(abs(rect.x_min), abs(rect.x_max)))
            array = np.zeros((h, w), dtype=bool)
            setRangeValue(array, True, rect.x_min, rect.x_max, rect.y_min, rect.y_max)

        h, w = array.shape
        assert w % 2 == 0 and h % 2 == 0, f"Dimensions (w = {w}, h = {h}) must be even."
        self.pixels: np.ndarray[bool] = array

    def fromShape(self, r: Rectangle):
        h, w = 2 * ceil(max(abs(r.y_min), abs(r.y_max))), 2 * ceil(max(abs(r.x_min), abs(r.x_max)))
        array = np.zeros((h, w), dtype=bool)
        setRangeValue(array, self.pixels, r.x_min, r.x_max, r.y_min, r.y_max)
        return PixelShape(array=array)

    def __add__(self, other):
        h1, w1 = self.dim()
        h2, w2 = other.dim()
        array = np.zeros((max(h1, h2), max(w1, w2)), dtype=bool)
        setRangeValue(array, self.pixels, - w1 / 2, w1 / 2, - h1 / 2, h1 / 2)
        setRangeValue(array, other.pixels, - w2 / 2, w2 / 2, - h2 / 2, h2 / 2)
        return PixelShape(array)

    def getOuterRectangle(self) -> Rectangle:
        # empty shape
        if self.isEmpty():
            return Rectangle(0, 0, 0, 0)
        h, w = self.pixels.shape
        ind = np.unravel_index(np.argmax(self.pixels), self.pixels.shape)[0]
        y_max = h / 2 - ind
        temp = np.rot90(self.pixels[ind:])
        ind = np.unravel_index(np.argmax(temp), temp.shape)[0]
        x_max = w / 2 - ind
        temp = np.rot90(temp[ind:])
        ind = np.unravel_index(np.argmax(temp), temp.shape)[0]
        y_min = ind - h / 2
        temp = np.rot90(temp[ind:])
        x_min = np.unravel_index(np.argmax(temp), temp.shape)[0] - w / 2
        return Rectangle(x_min, x_max, y_min, y_max)

    def getInnerRectangle(self, strategy) -> Rectangle:
        return strategy.findInnerRectanglePixels(self)

    def cut(self, birectangle: BiRectangle, strategy):
        return strategy.cutPixels(self, birectangle)

    def isPointInShape(self, x: float, y: float) -> bool:
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

        return any(0 <= x < w and 0 <= y < h and self.pixels[y, x] for x in xs_to_check for y in ys_to_check)

    def resize(self, min_w: int = 2, min_h: int = 2):
        assert min_w % 2 == 0, f"Minimum width {min_w} must be even."
        assert min_h % 2 == 0, f"Minimum height {min_h} must be even."
        h, w = self.dim()
        new_w = max(min_w, w)
        new_h = max(min_h, h)
        res = np.zeros((new_h, new_w))
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
        x1 = x1 + w1 / 2
        y2 = h2 / 2 - y2
        x2 = x2 + w2 / 2
        return y1.shape == y2.shape and x1.shape == x2.shape and np.all(y1 == y2) and np.all(x1 == x2)

    def width(self) -> int:
        return self.pixels.shape[1]

    def height(self) -> int:
        return self.pixels.shape[0]

    def isEmpty(self) -> bool:
        return not self.pixels.any()

    def dim(self) -> tuple[int, int]:
        return self.pixels.shape

    def plot(self) -> None:
        h, w = self.dim()
        mat_to_plot = self.grayscale()
        # transparency when not a black pixel
        alpha = np.ones(mat_to_plot.shape)
        alpha[mat_to_plot != 0] = 0
        plt.imshow(mat_to_plot, cmap='gray', vmin=0, vmax=255, alpha=alpha, extent=(- w / 2, w / 2, - h / 2, h / 2))

    def toImage(self, name: str = "default.bmp"):
        if not name.endswith(".bmp"):
            name += ".bmp"
        img = Image.fromarray(self.grayscale(), 'L')
        img.save('resources/' + name)

    def grayscale(self) -> np.ndarray:
        return np.uint8((1 - self.pixels) * 255)

    def toSinogram(self, maxAngle: float = 180.):
        # useful ?
        # array = rescale(array, scale=0.4, mode='reflect', channel_axis=None)

        theta = np.linspace(0.0, maxAngle, max(self.pixels.shape), endpoint=False)
        sinogram = radon(self.pixels, theta=theta)
        return sinogram

        # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
        #
        # ax1.set_title("Original")
        # ax1.imshow(self.pixels, cmap=plt.cm.Greys_r)
        # dx, dy = 0.5 * 180.0 / max(self.pixels.shape), 0.5 / sinogram.shape[0]
        # ax2.set_title("Radon transform\n(Sinogram)")
        # ax2.set_xlabel("Projection angle (deg)")
        # ax2.set_ylabel("Projection position (pixels)")
        # ax2.imshow(
        #     sinogram,
        #     cmap=plt.cm.Greys_r,
        #     extent=(-dx, maxAngle + dx, -dy, sinogram.shape[0] + dy),
        #     aspect='auto',
        # )
        # fig.tight_layout()
        # plt.show()
