from src.view.ViewInterface import ViewInterface
from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.tomography.TomographyMethod import TomographyMethod
from src.shapes.pixelShape import PixelShape
from src.utils import resize2D,toImage

class ShapeAnalogyModel:
    def __init__(self):
        self.shapes = [None] * 3
        self.result = None
        self.views = []
        self.methods : BiRectangleMethod | TomographyMethod = {
            "bi-rectangle method": BiRectangleMethod(),
            "tomography method": TomographyMethod()
        }
        self.analogyMethod = self.methods["bi-rectangle method"]

    def addObserver(self, view: ViewInterface):
        self.views.append(view)
        
    def can_start(self):
        return all(s is not None for s in self.shapes)

    def startAnalogy(self):
        if self.can_start():
            self.result, full_array = self.analogyMethod.analogy(*self.shapes)
            if self.result is not None:
                self.result.toImage()
                event="S"
            if full_array is not None:
                arr = resize2D(full_array, 300, 300)
                #toImage(arr)
            else:
                event = "NS"
            self.notify(event)

    def setShape(self, indice:int, filePath:str):
        self.result = None
        self.shapes[indice] = PixelShape(img=filePath)
        self.notify(None)

    def removeShape(self, indice:int):
        self.shapes[indice] = None
        self.notify(None)

    def hasResult(self):
        return self.result is not None


    def notify(self,event:str):
        for view in self.views:
               view.react(event)

    
    def change_method(self,method):
        self.analogyMethod = self.methods[method]
        self.notify(None)
    
    def get_birectangle_cutting_strategy(self) -> list:
        return self.analogyMethod.get_cutting_method()
    
    def set_birectangle_cutting_strategy(self,strategy) -> None: 
        self.analogyMethod.set_cutting_method(strategy)
        
    def get_birectangle_cutting_strategy_values(self) -> str:
        return self.analogyMethod.get_cutting_values()
    
    
    def get_birectangle_birectangleAnalogy_strategy(self):
        return self.analogyMethod.get_birectangle_analogy_method()
    
    def set_birectangle_birectangleAnalogy_strategy(self,strategy):
        self.analogyMethod.set_birectangle_analogy_method(strategy)
    
    def get_birectangle_birectangleAnalogy_strategy_values(self):
        return self.analogyMethod.get_birectangleAnalogy_values()
    
    
    def get_birectangle_inner_rectangle_finder_strategy(self):
        return self.analogyMethod.get_inner_rectangle_finder_method()
    def set_birectangle_inner_rectangle_finder_strategy(self,strategy):
        self.analogyMethod.set_inner_rectangle_finder_method(strategy)
    def get_birectangle_inner_rectangle_finder_strategy_values(self):
        return self.analogyMethod.get_inner_rectangle_finder_values()