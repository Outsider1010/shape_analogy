from tkinter import ttk,DISABLED,NORMAL
from PIL import Image, ImageTk, ImageOps
from src.view.ViewInterface import ViewInterface
import pathlib, os

class StartView(ttk.Button, ViewInterface):
    def __init__(self, parent, model):
        ttk.Button.__init__(self, parent)
        ViewInterface.__init__(self, model)
        img_file_name = "../../resources/play.png"
        current_dir = pathlib.Path(__file__).parent.resolve() 
        img_path = os.path.join(current_dir, img_file_name)
        imageStart = Image.open(img_path)
        image = ImageOps.contain(imageStart, (100,50), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.config(image=photo,state=DISABLED,command=self.start)
        self.image = photo
    def start(self):
        if self.model.can_Start():
            self.model.startAnalogy()
    def reagir(self):
        print("je réagis")
        if self.model.can_Start():
            print("je suis actif ")
            self.config(state=NORMAL)
        else:
            print("je suis inactif")
            self.config(state=DISABLED)
    def start(self):
        print("je demarre l'analogie")
        self.model.startAnalogy()