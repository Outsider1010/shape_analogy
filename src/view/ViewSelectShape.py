from tkinter import ttk, Label, BOTH
from PIL import Image, ImageTk,ImageOps
from tkinter.filedialog import askopenfilename
from src.view.ViewInterface import ViewInterface

class ViewSelectShape(ttk.Frame, ViewInterface):

    def __init__(self, parent, number,model):
        ttk.Frame.__init__(self,parent)
        ViewInterface.__init__(self,model)
        self.label = None
        self.deleteButton = None
        self.number = number
        self.button = ttk.Button(self, text=f"select shape {chr(ord('A')+number)}", command = self.displayImage)
        self.button.place(relx=0.5, rely=0.5, anchor="center")
        self.path = None
        self.pack_propagate(False)
      
      
    def displayImage(self):
        shapeFile = askopenfilename(filetypes=[("BMP files","*.bmp")])
        if shapeFile!=() and shapeFile != "":
            self.model.setShape(self.number,shapeFile)
            self.set_image(shapeFile)
     
    def create_image(self):
        self.model.toImage(self.number,self.path)
    def resize(self, event):
        if self.path is not None:
            
            largeur, hauteur = self.winfo_width(), self.winfo_height()
            # Redimensionner l'image tout en conservant le rapport d'aspect
            image = ImageOps.contain(self.model.toImage(self.number,self.path), (largeur,hauteur), Image.Resampling.LANCZOS)
        
            # Créer une nouvelle image avec un fond blanc
            new_image = Image.new("RGB", (largeur,hauteur), (255, 255, 255))
            # Calculer la position pour centrer l'image
            x_offset = (largeur - image.width) // 2
            y_offset = (hauteur - image.height) // 2
            new_image.paste(image, (x_offset, y_offset))
            photo = ImageTk.PhotoImage(new_image)
            self.label.config(image=photo)
            self.label.image = photo


    def set_image(self, image_path):
        self.button.place_forget()
        self.path = image_path
        self.label = Label(self)
        self.label.pack(fill=BOTH,expand=True)
        self.label.configure(relief='solid',borderwidth =2)
        # On ajoute un événement pour redimensionner l'image quand le cadre change de taille
        self.bind("<Configure>", self.resize)
        self.resize((self.winfo_width(), self.winfo_height()))
        
        img_file_name = "resources/delete.png"
        imageDelete = Image.open(img_file_name)
        image = ImageOps.contain(imageDelete, (20,20), Image.Resampling.LANCZOS)   
        photo = ImageTk.PhotoImage(image)
        self.deleteButton = ttk.Button(self, width=100, command=self.unset_image)
        self.deleteButton.config(image=photo)
        self.deleteButton.image = photo
        self.deleteButton.place(relx=0,rely=0)
    
        
    def unset_image(self):
        self.path = None
        self.label.destroy()
        self.model.removeShape(self.number)
        self.deleteButton.destroy()
        self.button.place(relx=0.5, rely=0.5, anchor="center")
    def react(self,event:str):
        print(self.path,self.number)
        if(self.path!=None):
            self.resize((0,0))