from src.shape_analogy import ShapeAnalogy
from src.view.ViewInterface import ViewInterface
from src.birectangle.bi_rectangle_method import BiRectangleMethod
from src.tomography.tomography_method import TomographyMethod
from src.shapes.pixel_shape import PixelShape
from src.utils import resize2D


class ShapeAnalogyModel:
    def __init__(self):
        self.shapes = [None] * 3
        self.result = None
        self.views = []
        self.methods : dict[str, ShapeAnalogy] = {
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
                self.resizeToCorrectSize()
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

    def notify(self, event: str | None):
        for view in self.views:
               view.react(event)

    def change_method(self,method):
        self.analogyMethod = self.methods[method]
        self.notify(None)
    
    def save_result(self,save_path):
       self.result.toImage(save_path)
    
    def resizeToCorrectSize(self):
        maxWidth = max(self.shape[2],max(self.shape[0],self.shape[1],key=lambda x: x.width()),key = lambda x:x.width())
        maxHeight = max(self.shape[2],max(self.shape[0],self.shape[1],key=lambda x: x.height()),key = lambda x:x.height())
        self.result.resize(maxWidth + (maxWidth%2),maxHeight+maxWidth%2)
        
    def getMethod(self):
        return self.analogyMethod
   