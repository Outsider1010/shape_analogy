from tkinter import ttk
from src.view.ViewInterface import ViewInterface
from src.view.startView import StartView
from src.view.ViewShape import ViewShape
from src.view.OptionView import OptionView
class MainView(ttk.Frame,ViewInterface):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent)
        ViewInterface.__init__(self, model)
        self.tomographicView = None
        self.shapeFrame = ViewShape(self, model)
        self.shapeFrame.pack(fill="both", expand=True, padx=150, pady=80)
        self.startView = StartView(self, model)
        self.startView.pack(side="bottom", pady=20)
        self.optionView = OptionView(self,self.model)
