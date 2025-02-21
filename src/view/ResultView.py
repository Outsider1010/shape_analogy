from tkinter import ttk,Label,BOTH
from PIL import Image, ImageTk,ImageOps
from src.view.ViewInterface import ViewInterface
import pathlib, os

class ResultView(ttk.Frame, ViewInterface):

    def __init__(self, parent,model):
        ttk.Frame.__init__(self,parent)
        ViewInterface.__init__(self,model)
        self.label = Label(self)
        self.pack_propagate(False)
        self.configure(relief='solid', borderwidth=2)
        self.path = "../../resources/no_shape.bmp"
        current_dir = pathlib.Path(__file__).parent.resolve() 
        img_path = os.path.join(current_dir, self.path)
        self.set_image(img_path)

    def resize(self, event):
        if self.path is not None:
            current_dir = pathlib.Path(__file__).parent.resolve() 
            img_path = os.path.join(current_dir, self.path)
            image = Image.open(img_path)
            largeur, hauteur = self.winfo_width(), self.winfo_height()
            image = ImageOps.contain(image, (largeur,hauteur), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.label.config(image=photo)
            self.label.image = photo
    
    def set_image(self, image_path):
        """Met à jour l'affichage de l'image et l'adapte parfaitement à la taille du conteneur."""
        self.path = image_path
        self.label.destroy()
        self.label = Label(self)
        self.label.pack(fill=BOTH,expand=True)
        self.label.configure(relief='solid',borderwidth =2)
        # On ajoute un événement pour redimensionner l'image quand le cadre change de taille
        self.bind("<Configure>", self.resize)
        self.resize((self.winfo_width(), self.winfo_height()))

    def reagir(self):
        if self.model.hasResult():
            self.path = "../../resources/default.bmp"   
        else:
            self.path = "../../resources/no_shape.bmp"
        self.set_image(self.path)