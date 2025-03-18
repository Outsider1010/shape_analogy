from decimal import Decimal
from src.birectangle.Rectangle import Rectangle
from src.shapes.UnionRectangles import UnionRectangles

import numpy as np
import matplotlib.pyplot as plt


def test_single_pixel():
    r = Rectangle(Decimal('0'), Decimal('1'), Decimal('0'), Decimal('1'))
    union = UnionRectangles([r])
    pixels = union.toPixels()

    expected = np.array([[255]], dtype=np.uint8)
    assert np.array_equal(pixels, expected), f"Erreur : attendu {expected}, obtenu {pixels}"
    print("Test single pixel réussi.")


def test_partial_coverage():
    r = Rectangle(Decimal('0.5'), Decimal('1.5'), Decimal('0.5'), Decimal('1.5'))
    union = UnionRectangles([r])
    pixels = union.toPixels()

    expected = np.full((2, 2), 64, dtype=np.uint8)
    assert np.array_equal(pixels, expected), f"Erreur : attendu {expected}, obtenu {pixels}"
    print("Test partial coverage réussi.")


if __name__ == '__main__':
    test_single_pixel()
    test_partial_coverage()

    r_visual = Rectangle(Decimal('0'), Decimal('1'), Decimal('0'), Decimal('1'))
    union_visual = UnionRectangles([r_visual])
    pixels_visual = union_visual.toPixels()

    plt.imshow(pixels_visual, cmap='gray', origin='lower')
    plt.title("Affichage toPixels - Recouvrement partiel")
    plt.colorbar(label="Teinte (0-255)")
    plt.show()