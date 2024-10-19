class Point:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __repr__(self):
        return f"({self.x}, {self.y})"