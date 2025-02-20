from tkinter import ttk,Canvas,Label,NW,TOP,BOTH
from PIL import Image, ImageTk,ImageOps
import pathlib, os
from src.view.ViewInterface import ViewInterface 
class ViewSelectShape(ttk.Frame,ViewInterface):
    def __init__(self, parent, shapeSelector, number,model):
        ttk.Frame.__init__(self,parent)
        ViewInterface.__init__(self,model)  
        self.number = number
        self.shapeSelector = shapeSelector  
        self.button  = ttk.Button(self,text=f"select shape {number}",command = self.displayImage)
        self.button.place(relx=0.5, rely=0.5, anchor="center")
        self.path = "/home/alexis/Documents/pngwing.com.png"
        print("largeur",self.winfo_width())
        self.configure(relief='solid',borderwidth =2)
        self.pack_propagate(False)
      
    def displayImage(self):
        print("largeur",self.winfo_width())
        filename = self.shapeSelector()
        print(filename)
        if filename != () and filename != "":
          self.set_image(filename)
          
          
    def resize(self, event):
        if(self.path!=None):
            image = Image.open(self.path)
            
            
            largeur, hauteur = self.winfo_width(), self.winfo_height()
            
            
            image = ImageOps.contain(image, (largeur,hauteur), Image.Resampling.LANCZOS)
            
           
            photo = ImageTk.PhotoImage(image)
            
        
            self.label.config(image=photo)
            self.label.image = photo
        

    def set_image(self, image_path):
        """Met à jour l'affichage de l'image et l'adapte parfaitement à la taille du conteneur."""
        self.button.place_forget()
        self.path = image_path
        self.label = Label(self)
        self.label.pack(fill=BOTH,expand=True)
        self.label.configure(relief='solid',borderwidth =2)
        # On ajoute un événement pour redimensionner l'image quand le cadre change de taille
        self.bind("<Configure>", self.resize)
        self.resize((self.winfo_width(), self.winfo_height()))
        img_file_name = "../../resources/delete.png"
        current_dir = pathlib.Path(__file__).parent.resolve() 
        img_path = os.path.join(current_dir, img_file_name)
        imageDelete = Image.open(img_path)
        image = ImageOps.contain(imageDelete, (20,20), Image.Resampling.LANCZOS)   
        photo = ImageTk.PhotoImage(image)
        self.deleteButton = ttk.Button(self,width=100,command=self.unSet_Image)
        self.deleteButton.config(image=photo)
        self.deleteButton.image = photo
        self.deleteButton.place(relx=0,rely=0)
        
    def unSet_Image(self):
        self.path = None
        self.label.destroy()
        self.model.removeShape(self.number-1)
        self.deleteButton.destroy()
        self.button.place(relx=0.5, rely=0.5, anchor="center")
        
        
        