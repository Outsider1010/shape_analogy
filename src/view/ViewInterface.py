from abc import ABC


class ViewInterface(ABC):
    def __init__(self,model):
        self.model = model
        model.addObserver(self)

    def react(self,event:str):
        pass