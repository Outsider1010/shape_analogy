from tkinter import ttk
from src.view.ViewSelectShape import ViewSelectShape
from tkinter.filedialog import askopenfilename
from src.view.ResultView import ResultView

class ViewShape(ttk.Frame):
    def __init__(self, parent,model):
        self.model = model
        super().__init__(parent)
        self.grid(row=0, column=0, padx=5, pady=5)
        # Configure grid frame to use all available space
        for i in range(2):
            self.grid_rowconfigure(i, weight=1)  # Donne un poids égal aux lignes
            self.grid_columnconfigure(i, weight=1)  # Donne un poids égal aux colonnes

        # Create buttons with sticky option to fill their cells
        self.button1 = ViewSelectShape(self, self.selectFirstShape, 1,self.model)
        self.button1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.button2 = ViewSelectShape(self, self.selectSecondShape, 2,self.model)
        self.button2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.button3 = ViewSelectShape(self, self.selectThirdShape, 3,self.model)
        self.button3.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.empty_cell = ResultView(self,model)
        self.empty_cell.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
       
    def selectFirstShape(self):
        shapeFile = self.__ask()
        if shapeFile!=() and shapeFile != "":
            self.model.setShape(0,shapeFile)
        return shapeFile

    def selectSecondShape(self):
        shapeFile = self.__ask()
        if shapeFile!=() and shapeFile != "":
            self.model.setShape(1,shapeFile)
        return shapeFile

    def selectThirdShape(self):
        shapeFile = self.__ask()
        if shapeFile!=() and shapeFile != "":
            self.model.setShape(2,shapeFile)
        return shapeFile

    def __ask(self):
        return askopenfilename(filetypes=[("BMP files","*.bmp")])