from decimal import Decimal
from src.birectangle.rectangle import Rectangle
from src.shapes.union_rectangles import UnionRectangles

import numpy as np
import matplotlib.pyplot as plt


def test_single_pixel():
    """
        Test : Un rectangle qui recouvre entièrement un pixel.
        On crée un rectangle couvrant exactement [0, 1]x[0, 1].
        La grille sera de taille 2x2 (centrée sur l'origine), et seul le pixel (1,1) (en coordonnées matrice)
        sera entièrement recouvert, donc sa teinte doit être 0 (noir), et les autres 255 (blanc).
    """
    r = Rectangle(Decimal('0'), Decimal('1'), Decimal('0'), Decimal('1'))
    union_rect = UnionRectangles([r])
    pixels = union_rect.toPixels()

    # On vérifie que le pixel entièrement recouvert est noir.
    assert pixels[1, 1] == 0, f"Attendu 0 pour le pixel entièrement recouvert, obtenu {pixels[1,1]}"

    # On vérifie que les autres pixels restent blancs.
    assert pixels[0, 0] == 255, f"Attendu 255 pour le pixel non recouvert, obtenu {pixels[0,0]}"
    assert pixels[0, 1] == 255, f"Attendu 255 pour le pixel non recouvert, obtenu {pixels[0,1]}"
    assert pixels[1, 0] == 255, f"Attendu 255 pour le pixel non recouvert, obtenu {pixels[1,0]}"

    print("test_single_pixel passed.")


def test_partial_coverage():
    """
        Test : Un rectangle qui recouvre partiellement un pixel.
        Ici, on crée un rectangle couvrant [0, 1] en x et [0, 0.5] en y.
        Le pixel (1,1) de la grille (qui couvre [0,1]x[0,1]) sera recouvert à 50% (aire 0.5).
        La teinte attendue est : 255 - round(0.5*255) = 255 - 128 = 127 (avec round(127.5)=128).
    """
    r = Rectangle(Decimal('0'), Decimal('1'), Decimal('0'), Decimal('0.5'))
    union_rect = UnionRectangles([r])
    pixels = union_rect.toPixels()
    expected = 127

    assert pixels[1, 1] == expected, f"Attendu {expected} pour une couverture à 50%, obtenu {pixels[1,1]}"

    print("test_partial_coverage passed.")


if __name__ == '__main__':
    # Lancer les tests.
    test_single_pixel()
    test_partial_coverage()

    # Exemple avec plusieurs rectangles qui se chevauchent partiellement.
    r1 = Rectangle(Decimal('0.2'), Decimal('2.8'), Decimal('0.2'), Decimal('1.8'))
    r2 = Rectangle(Decimal('1.5'), Decimal('3.5'), Decimal('1.0'), Decimal('2.5'))
    r3 = Rectangle(Decimal('2.0'), Decimal('4.0'), Decimal('0.5'), Decimal('3.0'))
    union_visual = UnionRectangles([r1, r2, r3])
    pixels_visual = union_visual.toPixels()

    h, w = pixels_visual.shape
    extent = [-w / 2, w / 2, -h / 2, h / 2]

    plt.imshow(pixels_visual, cmap='gray', origin='lower', extent=extent)
    plt.title("Affichage toPixels - Union de plusieurs rectangles")
    plt.colorbar(label="Teinte (0-255)")

    # Affiche les rectangles.
    for rect in union_visual.rectangles:
        rect.plotBorder("orange", alpha=1.0, zorder=5)

    plt.show()