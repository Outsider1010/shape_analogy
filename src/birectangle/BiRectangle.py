from src.birectangle.Rectangle import Rectangle

class BiRectangle:
    def __init__(self, outerRectangle: Rectangle, innerRectangle: Rectangle):
        assert outerRectangle.containsRectangle(
            innerRectangle), (f"Inner rectangle should be contained by outer rectangle.\n"
                              f"Outer : {outerRectangle}\nInner : {innerRectangle}")

        self.innerRectangle = innerRectangle
        self.outerRectangle = outerRectangle

    def __repr__(self):
        return "Outer: " + str(self.outerRectangle) + " Inner: " + str(self.innerRectangle)

    def __str__(self):
        return "Outer: " + str(self.outerRectangle) + "\nInner: " + str(self.innerRectangle)

    def separate(self, epsilon: float):
        if self.innerRectangle.x_min == self.outerRectangle.x_min:
            self.innerRectangle.x_min += epsilon
        if self.innerRectangle.x_max == self.outerRectangle.x_max:
            self.innerRectangle.x_max -= epsilon
        if self.innerRectangle.y_min == self.outerRectangle.y_min:
            self.innerRectangle.y_min += epsilon
        if self.innerRectangle.y_max == self.outerRectangle.y_max:
            self.innerRectangle.y_max -= epsilon


