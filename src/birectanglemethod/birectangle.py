from src.birectanglemethod.rectangle import Rectangle

class BiRectangle:
    def __init__(self, outerRectangle: Rectangle, innerRectangle: Rectangle):
        assert outerRectangle.containsRectangle(
            innerRectangle), "Inner rectangle should be contained by outer rectangle"

        self.innerRectangle = innerRectangle
        self.outerRectangle = outerRectangle

    def __repr__(self):
        return "Outer: " + str(self.outerRectangle) + " Inner: " + str(self.innerRectangle)

    def __str__(self):
        return "Outer: " + str(self.outerRectangle) + "\nInner: " + str(self.innerRectangle)


