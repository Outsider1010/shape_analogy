from tkinter import ttk,Label,BOTH
from PIL import Image, ImageTk,ImageOps
from src.view.ViewInterface import ViewInterface
from tkinter.filedialog import asksaveasfile 

class ResultView(ttk.Frame,ViewInterface):

    def __init__(self, parent,model):
        ttk.Frame.__init__(self,parent)
        ViewInterface.__init__(self,model)
        self.deleteButton = None
        self.label = Label(self)
        self.pack_propagate(False)
        self.configure(relief='solid', borderwidth=2)
        self.path = "resources/no_shape.bmp"
        self.set_image()

    def resize(self, event):
        if self.path is not None:
            image = Image.open(self.path)
            largeur, hauteur = self.winfo_width(), self.winfo_height()
            # Redimensionner l'image tout en conservant le rapport d'aspect
            image = ImageOps.contain(image, (largeur,hauteur), Image.Resampling.LANCZOS)
        
            # Créer une nouvelle image avec un fond blanc
            new_image = Image.new("RGB", (largeur,hauteur), (255, 255, 255))
            # Calculer la position pour centrer l'image
            x_offset = (largeur - image.width) // 2
            y_offset = (hauteur - image.height) // 2
            new_image.paste(image, (x_offset, y_offset))
            photo = ImageTk.PhotoImage(new_image)
            self.label.config(image=photo)
            self.label.image = photo
        if self.model.hasResult():
            img_file_name = "resources/enregistre.png"
            imageDelete = Image.open(img_file_name)
            image = ImageOps.contain(imageDelete, (20,20), Image.Resampling.LANCZOS)   
            photo = ImageTk.PhotoImage(image)
            self.deleteButton = ttk.Button(self, width=100, command=self.save_image)
            self.deleteButton.config(image=photo)
            self.deleteButton.image = photo
            self.deleteButton.place(relx=0,rely=0)
    
    def save_image(self):
        save_path = asksaveasfile(filetypes = [('bmp', '*.bmp')] , defaultextension = 'bmp')
        if save_path != () and save_path != " ":
            self.model.save_result(save_path.name)
            
    def set_image(self):
        """Met à jour l'affichage de l'image et l'adapte parfaitement à la taille du conteneur."""
        self.label.destroy()
        self.label = Label(self)
        self.label.pack(fill=BOTH,expand=True)
        self.label.configure(relief='solid',borderwidth =2)
        # On ajoute un événement pour redimensionner l'image quand le cadre change de taille
        self.bind("<Configure>", self.resize)
        self.resize((self.winfo_width(), self.winfo_height()))

    def react(self,event:str):
        if(event == "NS"):
            self.path = "resources/noSolution.png"
            return
        if self.model.hasResult():
            self.path = "resources/default.bmp"   
        else:
            self.path = "resources/no_shape.bmp"
        self.set_image()