import tkinter as tk
from src.view.MainView import MainView
from src.ShapeAnalogyModel import ShapeAnalogyModel

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        model = ShapeAnalogyModel()
        view = MainView(self, model)
        # Récupérer les dimensions de l'écran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        view.pack(fill="both", expand=True)