import tkinter as tk
from src.view.MainView import MainView
from src.ShapeAnalogyModel import ShapeAnalogyModel

tomoGraphic = 1

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.model = ShapeAnalogyModel()
        self.view = MainView(self, self.model)
        self.view.pack(fill="both", expand=True)
        self.mainloop()