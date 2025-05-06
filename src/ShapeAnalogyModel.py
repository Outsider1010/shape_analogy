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
        self.working = False
        self.methods : dict[str, ShapeAnalogy] = {
            "bi-rectangle method": BiRectangleMethod(),
            "tomography method": TomographyMethod()
        }
        self.analogyMethod = self.methods["bi-rectangle method"]

    def addObserver(self, view: ViewInterface):
        self.views.append(view)
        
    def can_start(self):
        return all(s is not None for s in self.shapes) and not self.working 

    def startAnalogy(self):
        if self.can_start():
            self.working = True
            self.notify(None)
            self.result = self.analogyMethod.analogy(self.shapes[0],self.shapes[1],self.shapes[2])
            self.result = self.result.toPixels()
            print(self.result.dim(),self.shapes[1].dim())
            if self.result is not None:
                self.resizeToCorrectSize()
                self.result.toImage()
                event="S"
            else:
                event = "NS"
            self.working = False
            self.notify(event)

    def setShape(self, indice:int, filePath:str):
        self.result = None
        self.shapes[indice] = PixelShape(img=filePath)
        maxWidth = -1
        maxHeigth = -1
        for (indices,shapes) in enumerate(self.shapes):
            if(shapes != None):
                maxWidth = max(shapes.width(),maxWidth)
                maxHeigth = max(shapes.height(),maxHeigth)
        for (indice,shapes) in enumerate(self.shapes):
            if(self.shapes[indice]!= None):
                print("resize")
                print(shapes.width(),shapes.height())
                print(maxWidth,maxHeigth)
                self.shapes[indice] = self.shapes[indice].resize(maxWidth,maxHeigth)
                
        self.notify(None)
    def toImage(self,indice,path):
        return self.shapes[indice].toImage(False)
    def removeShape(self, indice:int):
        self.shapes[indice] = None
        maxWidth = -1
        maxHeigth = -1
        for (indices,shapes) in enumerate(self.shapes):
            if(shapes != None):
                maxWidth = max(shapes.width(),maxWidth)
                maxHeigth = max(shapes.height(),maxHeigth)
        for (indice,shapes) in enumerate(self.shapes):
            if(self.shapes[indice]!= None):
                self.shapes[indice] = self.shapes[indice].resize(maxWidth,maxHeigth)
            else:
                print("None")
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
        maxWidth = max(self.shapes[2],max(self.shapes[0],self.shapes[1],key=lambda x: x.width()),key = lambda x:x.width()).width()
        maxWidth = max(self.result.width(),maxWidth)

        maxHeight = max(self.shapes[2],max(self.shapes[0],self.shapes[1],key=lambda x: x.height()),key = lambda x:x.height()).height()
        maxHeight = max(self.result.height(),maxHeight)
        
        print(maxWidth/self.result.width(),maxHeight/self.result.height())
        self.shapes[0] = self.shapes[0].resize(maxWidth,maxHeight)
        self.shapes[1] = self.shapes[1].resize(maxWidth,maxHeight)
        self.shapes[2] = self.shapes[2].resize(maxWidth,maxHeight)
        self.result = self.result.resize(maxWidth + (maxWidth%2),maxHeight+maxWidth%2)
        
    def getMethod(self):
        return self.analogyMethod
   