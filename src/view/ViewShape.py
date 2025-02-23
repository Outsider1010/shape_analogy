from tkinter import ttk
from src.view.ViewSelectShape import ViewSelectShape
from src.view.ResultView import ResultView

class ViewShape(ttk.Frame):
    def __init__(self, parent,model):
        self.model = model
        super().__init__(parent)
        self.grid(row=0, column=0, padx=5, pady=5)
        for i in range(2):
            self.grid_rowconfigure(i, weight=1)  
            self.grid_columnconfigure(i, weight=1)  

        
        self.button1 = ViewSelectShape(self,  0,self.model)
        self.button1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.button2 = ViewSelectShape(self,  1,self.model)
        self.button2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.button3 = ViewSelectShape(self, 2,self.model)
        self.button3.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.empty_cell = ResultView(self,model)
        self.empty_cell.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
       
  
   
