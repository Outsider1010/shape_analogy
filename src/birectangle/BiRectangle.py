from src.birectangle.Rectangle import Rectangle

class BiRectangle:
    def __init__(self, outerRectangle: Rectangle, innerRectangle: Rectangle):
        assert outerRectangle.containsRectangle(
            innerRectangle), (f"Inner rectangle should be contained by outer rectangle.\n"
                              f"Outer : {outerRectangle}\nInner : {innerRectangle}")

        self.innerRectangle: Rectangle = innerRectangle
        self.outerRectangle: Rectangle = outerRectangle

    def __repr__(self):
        return "Outer: " + str(self.outerRectangle) + " / Inner: " + str(self.innerRectangle)

    def __iter__(self):
        return iter((self.innerRectangle, self.outerRectangle))

    def separate(self, epsilon: float) -> None:
        innerR, outerR = self
        innerR.set_x(innerR.x_min + epsilon * (innerR.x_min == outerR.x_min),
                     innerR.x_max - epsilon * (innerR.x_max == outerR.x_max))
        innerR.set_y(innerR.y_min + epsilon * (innerR.y_min == outerR.y_min),
                     innerR.y_max - epsilon * (innerR.y_max == outerR.y_max))