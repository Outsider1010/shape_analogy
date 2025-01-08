from shape import shape_analogy_from_file
from rectangle import Rectangle, rects_to_array
from utils.utils import array_to_image

shape_analogy_from_file("resources/test2.bmp", "resources/res.bmp",
                        "resources/test1.bmp" )

# array_to_image(rects_to_array(Rectangle(-2, 2, -1, 1),
#                               Rectangle(-1, 1, -2, -1)), "test2.bmp")