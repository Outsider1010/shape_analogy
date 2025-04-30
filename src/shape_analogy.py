from abc import ABC
from src.shapes.shape import Shape

class ShapeAnalogy(ABC):
    """
    Interface for the different methods to perform shape analogies
    """
    def analogy(self, SA : Shape, SB : Shape, SC : Shape) -> Shape:
        """
        Performs the analogy and return if it finds one, a solution.
        :param SA: shape A
        :param SB: shape B
        :param SC: shape C
        :return: a solution to the analogical equation A : B :: C : ?
        """
        pass