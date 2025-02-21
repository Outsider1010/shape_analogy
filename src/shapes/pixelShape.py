import numpy as np
from math import ceil

from skimage.transform import radon

from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.Rectangle import Rectangle
from . shape import Shape
from PIL import Image

from ..utils import resize, toImage


# DO NOT IMPORT STRATEGIES

class PixelShape(Shape):
    """
    Representation of shapes using a boolean matrix with even dimensions.
    Each pixel is a square of length 1 and equals True if it is included in the shape
    """

    def __init__(self, array=None, img=None, rect=None, min_w = 2, min_h = 2):
        assert (array is not None) or (img is not None) or (rect is not None), \
               "One of the parameters (array, img or rect) must be set"

        if img is not None:
            array = np.array(Image.open(img)) == 0

        if rect is not None:
            h, w = (ceil(max(2 * abs(rect.y_min), 2 * abs(rect.y_max), min_h)),
                    ceil(max(2 * abs(rect.x_min), 2 * abs(rect.x_max), min_w)))
            if w % 2 != 0:
                w += 1
            if h % 2 != 0:
                h += 1
            array = np.zeros((h, w), dtype=bool)
            array[int(h / 2 - rect.y_max):ceil(h / 2 - rect.y_min), int(rect.x_min + w / 2):ceil(rect.x_max + w / 2)] = True

        w, h = array.shape
        assert w % 2 == 0 and h % 2 == 0, f"Dimensions (w = {h}, h = {w}) must be even."
        self.pixels: np.ndarray[bool] = array

    def fromShape(self, r: Rectangle):
        h, w = ceil(max(2 * abs(r.y_min), 2 * abs(r.y_max))), ceil(max(2 * abs(r.x_min), 2 * abs(r.x_max)))
        if w % 2 != 0:
            w += 1
        if h % 2 != 0:
            h += 1
        array = np.zeros((h, w), dtype=bool)
        self.__set_values_from_this(array, r.x_min, r.x_max, r.y_min, r.y_max)
        return PixelShape(array=array)

    def __set_values_from_this(self, arr, x_min, x_max, y_min, y_max):
        h1, w1 = arr.shape
        b1 = ceil(h1 / 2 - y_min)
        b2 = int(h1 / 2 - y_max)
        b3 = int(x_min + w1 / 2)
        b4 = ceil(x_max + w1 / 2)

        h, w = self.dim()
        c1 = ceil(h / 2 - y_min)
        c2 = int(h / 2 - y_max)
        c3 = int(x_min + w / 2)
        c4 = ceil(x_max + w / 2)

        arr[b2:b1, b3:b4] |= self.pixels[c2:c1, c3:c4]

    def __add__(self, other):
        h1, w1 = self.dim()
        h2, w2 = other.dim()
        array = np.zeros((max(h1, h2), max(w1, w2)), dtype=bool)
        self.__set_values_from_this(array, - w1 / 2, w1 / 2, - h1 / 2, h1 / 2)
        other.__set_values_from_this(array, - w2 / 2, w2 / 2, - h2 / 2, h2 / 2)
        return PixelShape(array)

    def getOuterRectangle(self) -> Rectangle:
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

    def toPixelShape(self):
        return self

    def isPointInShape(self, x: float, y:float) -> bool:
        return self.pixels[int(self.height() / 2 - y), int(x + self.width() / 2)]

    def resize(self, min_w = 2, min_h = 2):
        return PixelShape(array=resize(self.pixels, min_w, min_h))

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
        return y1.shape == y2.shape and x1.shape == x2.shape and np.all(y1 == y2)  and np.all(x1 == x2)

    def width(self) -> int:
        return self.pixels.shape[1]

    def height(self) -> int:
        return self.pixels.shape[0]

    def isEmpty(self) -> bool:
        return not self.pixels.any()

    def dim(self) -> tuple[int, int]:
        return self.pixels.shape

    def toImage(self, name="default.bmp"):
        toImage(np.uint8((1 - self.pixels) * 255), name=name)

    def toSinogram(self, maxAngle = 180.):
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
