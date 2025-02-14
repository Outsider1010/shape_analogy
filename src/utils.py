import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.transform import radon

# Black -> True
# Anything else -> False
def image_to_array(img):
    return np.where(np.array(Image.open(img)) == 0, True, False)


def array_to_image(array, name="default.bmp"):
    img = Image.fromarray(np.uint8(np.where(array, 0, 255)), 'L')
    img.save('resources/'+name)


def arr_set_range_value_from_array(arr, x_min, x_max, y_min, y_max, fromArray):
    w, h = arr.shape
    b1 = int(y_min + w / 2)
    b2 = b1 + round(y_max - y_min)
    b3 = int(x_min + h / 2)
    b4 = b3 + round(x_max - x_min)

    w, h = fromArray.shape
    c1 = int(y_min + w / 2)
    c2 = c1 + round(y_max - y_min)
    c3 = int(x_min + h / 2)
    c4 = c3 + round(x_max - x_min)
    arr[b1:b2, b3:b4] |= fromArray[c1:c2, c3:c4]


def plot_sinogram(image):
    image = image_to_array(image)
    # image = rescale(image, scale=0.4, mode='reflect', channel_axis=None)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))

    ax1.set_title("Original")
    ax1.imshow(image, cmap=plt.cm.Greys_r)

    theta = np.linspace(0.0, 180.0, max(image.shape), endpoint=False)
    sinogram = radon(image, theta=theta)
    dx, dy = 0.5 * 180.0 / max(image.shape), 0.5 / sinogram.shape[0]
    ax2.set_title("Radon transform\n(Sinogram)")
    ax2.set_xlabel("Projection angle (deg)")
    ax2.set_ylabel("Projection position (pixels)")
    ax2.imshow(
        sinogram,
        cmap=plt.cm.Greys_r,
        extent=(-dx, 180.0 + dx, -dy, sinogram.shape[0] + dy),
        aspect='auto',
    )

    fig.tight_layout()
    plt.show()
