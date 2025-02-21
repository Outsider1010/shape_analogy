from src.view.ViewInterface import ViewInterface
from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.shapes.pixelShape import PixelShape
from src.birectangle.birectangleanalogy.SigmoidTopLeftAnalogy import SigmoidTopLeftAnalogy
from src.utils import resize2D,toImage

class ShapeAnalogyModel:
    def __init__(self):
        self.shapes = [None] * 3
        self.result = None
        self.analogyMethod = BiRectangleMethod(BRAnalogy= SigmoidTopLeftAnalogy)
        self.views = []

    def addObserver(self, view: ViewInterface):
        print("j'ajoute une vue")
        self.views.append(view)
        
    def can_Start(self):
        return all(s is not None for s in self.shapes)

    def startAnalogy(self):
        if self.can_Start:
            print("je lance l'analogie")
            self.result, full_array = self.analogyMethod.analogy(*self.shapes)
            if self.result is not None:
                self.result.toImage()
            if full_array is not None:
                arr = resize2D(full_array, 300, 300)
                toImage(arr)
            else:
                print("no solution")
            self.notifier()

    def setShape(self, indice, filePath):
        self.result = None
        self.shapes[indice] = PixelShape(img=filePath)
        self.notifier()

    def removeShape(self, indice):
        self.shapes[indice] = None
        self.notifier()

    def hasResult(self):
        return self.result is not None

    def notifier(self):
        for view in self.views:
               view.reagir()