import numpy as np
from math import ceil

from skimage.transform import radon

from src.biframemethod.birectangle import BiRectangle
from src.biframemethod.rectangle import Rectangle
from . shape import Shape
from PIL import Image
# DO NOT IMPORT STRATEGIES

class PixelShape(Shape):
    """
    Representation of shapes using a boolean matrix.
    Each pixel is a square of length 1 and equals True if it is included in the shape
    """

    def __init__(self, array=None, img=None, rect=None):
        assert (array is not None) or (img is not None) or (rect is not None), \
               "One of the parameters (array, img or rect) must be set"
        if img is not None:
            array = np.where(np.array(Image.open(img)) == 0, True, False)

        if rect is not None:
            w, h = (ceil(max(2 * abs(rect.y_min), 2 * abs(rect.y_max))),
                    ceil(max(2 * abs(rect.x_min), 2 * abs(rect.x_max))))
            array = np.zeros((w, h), dtype=bool)
            print(rect.y_min, rect.y_max, rect.x_min, rect.x_max)
            array[int(w / 2 - rect.y_max):int(w / 2 - rect.y_min), int(rect.x_min + h / 2):int(rect.x_max + h / 2)] = True

        self.pixels: np.ndarray[bool] = array


    def fromShape(self, x_min, x_max, y_min, y_max):
        array = np.zeros((ceil(max(2 * abs(y_min), 2 * abs(y_max))),
                                ceil(max(2 * abs(x_min), 2 * abs(x_max)))), dtype=bool)
        self.__set_values_from_this(array, x_min, x_max, y_min, y_max)
        return PixelShape(array=array)

    def __set_values_from_this(self, arr, x_min, x_max, y_min, y_max):
        w, h = arr.shape
        b1 = int(y_min + w / 2)
        b2 = b1 + round(y_max - y_min)
        b3 = int(x_min + h / 2)
        b4 = b3 + round(x_max - x_min)

        w, h = self.dim()
        c1 = int(y_min + w / 2)
        c2 = c1 + round(y_max - y_min)
        c3 = int(x_min + h / 2)
        c4 = c3 + round(x_max - x_min)
        arr[b1:b2, b3:b4] |= self.pixels[c1:c2, c3:c4]

    def merge(self, other):
        w1, h1 = self.dim()
        w2, h2 = other.dim()
        # no need to create a new shape
        if w1 >= w2 and h1 >= h2:
            other.__set_values_from_this(self.pixels, - h2/2, h2/2, - w2 / 2, w2 / 2)
            return self
        elif w2 >= w1 and h2 >= h1:
            self.__set_values_from_this(other.pixels, - h1/2, h1/2, - w1/2, w1/2)
            return other
        else:
            array = np.zeros((max(w1, w2), max(h1, h2)), dtype=bool)
            self.__set_values_from_this(array, -h1/2, h1/2, -w1/2, w1/2)
            other.__set_values_from_this(array, - h2/2, h2/2, - w2 / 2, w2 / 2)
            return PixelShape(array=array)


    def getOuterFrame(self) -> Rectangle:
        w, h = self.pixels.shape
        ind = np.unravel_index(np.argmax(self.pixels), self.pixels.shape)[0]
        y_max = w / 2 - ind
        temp = np.rot90(self.pixels[ind:])
        ind = np.unravel_index(np.argmax(temp), temp.shape)[0]
        x_max = h / 2 - ind
        temp = np.rot90(temp[ind:])
        ind = np.unravel_index(np.argmax(temp), temp.shape)[0]
        y_min = ind - w / 2
        temp = np.rot90(temp[ind:])
        x_min = np.unravel_index(np.argmax(temp), temp.shape)[0] - h / 2
        return Rectangle(x_min, x_max, y_min, y_max)

    def getInnerFrame(self, strategy) -> Rectangle:
        return strategy.findInnerFramePixels(self)

    def cut(self, birectangle: BiRectangle, strategy):
        return strategy.cutPixels(self, birectangle)

    def isPointInShape(self, x: float, y: float) -> bool:
        return self.pixels[int(self.width() / 2 - y), int(x + self.height() / 2)]

    def __eq__(self, other):
        if not isinstance(other, PixelShape):
            return False
        w1, h1 = self.pixels.shape
        w2, h2 = other.pixels.shape
        w = max(w1, w2)
        h = max(h1, h2)
        new_self_pixels = np.zeros((w, h), dtype=bool)
        new_other_pixels = np.zeros((w, h), dtype=bool)
        self.__set_values_from_this(new_self_pixels, - h1/2, h1/2, -w1/2, w1/2)
        other.__set_values_from_this(new_other_pixels, -h2/2, h2/2, -w2/2, w2/2)
        return np.all(new_self_pixels == new_other_pixels)

    def width(self) -> int:
        return self.pixels.shape[0]

    def height(self) -> int:
        return self.pixels.shape[1]

    def isEmpty(self) -> bool:
        return not self.pixels.any()

    def dim(self) -> tuple[int, int]:
        return self.pixels.shape

    def toImage(self, name="default.bmp"):
        img = Image.fromarray(np.uint8(np.where(self.pixels, 0, 255)), 'L')
        img.save('resources/' + name)

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

    def pixelsMatrix(self):
        return self.pixels
