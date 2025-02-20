from tkinter import ttk
from src.view.BirectangleView import BirectangleView
from src.view.ViewInterface import ViewInterface
from src.view.startView import StartView

class MainView(ttk.Frame, ViewInterface):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent)
        ViewInterface.__init__(self, model)
        self.BirectanglesView = BirectangleView(self,model)
        self.tomographicView = None
        self.mode = 0
        self.biRectanglesMode()
        self.startView = StartView(self, model)
        
        self.startView.pack(side="bottom",pady=20)
       
    def tomographicMode(self):
        pass
    def biRectanglesMode(self):
        if self.mode==1:
            self.tomographicView.forget_pack()
        self.BirectanglesView.pack(fill="both", expand=True)
        #StartView 
        