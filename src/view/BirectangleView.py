from tkinter import ttk, Label, W, Entry, Toplevel
from src.view.ViewShape import ViewShape
from src.view.ViewInterface import ViewInterface
from src.view.strategyViews.strategyView import StrategyView

class BirectangleView(ttk.Frame, ViewInterface):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent)
        ViewInterface.__init__(self, model)
        self.shapeFrame = ViewShape(self, model)
        self.shapeFrame.pack(fill="both", expand=True, padx=150, pady=80)
