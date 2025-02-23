from tkinter import ttk,DISABLED,NORMAL
from PIL import Image, ImageTk, ImageOps
from src.view.ViewInterface import ViewInterface


class StartView(ttk.Button, ViewInterface):

    def __init__(self, parent, model):
        ttk.Button.__init__(self, parent)
        ViewInterface.__init__(self, model)
        img_file_name = "resources/play.png"
       
        imageStart = Image.open(img_file_name)
        image = ImageOps.contain(imageStart, (100,50), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.config(image=photo, state=DISABLED, command=self.start)
        self.image = photo


    def start(self):
        if self.model.can_start():
            self.model.startAnalogy()


    def react(self,event:tuple):
        print(self.model.can_start())
        if self.model.can_start():
            self.config(state=NORMAL)
        else:
            self.config(state=DISABLED)
