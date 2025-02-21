from src.view.ViewInterface import ViewInterface
from src.birectanglemethod.BiRectangleMethod import BiRectangleMethod
from src.shapes.shape import Shape
from src.shapes.pixelShape import PixelShape
from src.birectangle.birectangleanalogy.SigmoidTopLeftAnalogy import SigmoidTopLeftAnalogy
class ShapeAnalogyModel:
    def __init__(self):
        self.shapes = [None]*3
        self.result = None
        self.analogyMethod = BiRectangleMethod(BRAnalogy= SigmoidTopLeftAnalogy)
        self.view = []
    def addObserver(self,view:ViewInterface):
        print("j'ajoute une vue")
        self.view.append(view)
        
    def can_Start(self):
        return self.shapes[0] != None and self.shapes[1] != None and self.shapes[2] != None
    def startAnalogy(self):
        if(self.can_Start):
           

            print("je lance l'analogie")
            self.result, full_array = m.analogy(self.shapes[0], self.shapes[1], self.shapes[2])
            if(self.result !=None):
                self.result.toImage()
            if full_array is not None:
                arr = resize2D(full_array, 300, 300)
                toImage(arr)
            else:
                print("no solution")
            self.notifier()
    def setShape(self,indice,filePath):
        if(self.result != None):
            self.result = None       
        self.shapes[indice] = PixelShape(img=filePath)
        self.notifier()
    def removeShape(self,indice):
        self.shapes[indice] = None
        self.notifier()
    def hasResult(self):
        return self.result != None
    def notifier(self):
        for view in self.view:
               view.reagir()