from abc import ABC
from src.ShapeAnalogy import ShapeAnalogy
class ViewInterface(ABC):
    def __init__(self,model:ShapeAnalogy):
        self.model = model
        model.addObserver(self)

    def react(self,event:str):
        pass