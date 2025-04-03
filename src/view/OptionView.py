from tkinter import ttk,Toplevel,Label,Button,Spinbox,StringVar,Radiobutton,Entry,Scale
from src.ShapeAnalogyModel import ShapeAnalogyModel
from PIL import Image, ImageTk,ImageTk,ImageOps
from src.birectangle.cuttingmethod.cut_in_8 import CuttingIn8

from src.birectangle.rectangleanalogy.center_dim_analogy import CenterDimAnalogy
from src.birectangle.rectangleanalogy.top_left_dim_analogy import TopLeftDimAnalogy
from src.birectangle.birectangleanalogy.ext_sigmoid_analogy import ExtSigmoidAnalogy
from src.birectangle.rectangleanalogy.area_analogy import AreaAnalogy
from src.birectangle.rectangleanalogy.coord_analogy import CoordAnalogy

from src.birectangle.cuttingmethod.cut_in_4_equal_parts_1 import CutIn4EqualParts1
from src.birectangle.birectangleanalogy.simple_analogy import SimpleAnalogy
from src.birectangle.cuttingmethod.horizontal_cut import HorizontalCut
from src.birectangle.cuttingmethod.vertical_cut import VerticalCut
from src.birectangle.cuttingmethod.sides_non_disjoint_cut import SidesNonDisjointCut
from src.birectangle.innerrectanglefinder.largest_rectangle_finder import LargestRectangleFinder
from src.birectangle.birectangleanalogy.bi_segment_analogy import BiSegmentAnalogy
# Define the classes representing the options
class BiRectangleOption():

    def __init__(self,root,model:ShapeAnalogyModel):
        self.model = model
        self.root = root
        self.windows = None
        self.birectangleAnalogyStrategy = {
            "Extended sigmoid":ExtSigmoidAnalogy,
            "BiSegment Analogy":BiSegmentAnalogy,
            "Simple Analogy":SimpleAnalogy,
        }
        self.cuttingStrategy = {
            "Cut4":CutIn4EqualParts1,
            "Cut8":CuttingIn8,
            "Horizontal cut":HorizontalCut,
            "Vertical cut":VerticalCut,
            "Non disjoint cut":SidesNonDisjointCut,
            
        }
        self.innerRectangleFinderStrategy = {
            "Largest rectangle": LargestRectangleFinder,
        }
    
        self.rectangleAnalogyStrategy = {
            "Center dimension analogy": CenterDimAnalogy,
            "Top left dimension analogy": TopLeftDimAnalogy,
            "Coords Analogy":CoordAnalogy,
            "Area Analogy":AreaAnalogy
        }
        


    def show(self):
        self.windows = Toplevel(self.root)
        self.setupWindows()

    def is_open(self):
        return self.windows is not None and self.windows.winfo_exists()
    def hide(self):
        if(self.windows):
            self.windows.destroy()   
    def select_analogy_strategy(self,event):
        self.model.set_birectangle_birectangleAnalogy_strategy(self.birect_analogy_combo.get())

    def select_cutting_strategy(self,event):
        self.model.set_birectangle_cutting_strategy(self.birect_cutting_combo.get())

    def select_inner_rectangle_finder_strategy(self,event):
        self.model.set_birectangle_inner_rectangle_finder_strategy(self.birect_inner_rectangle_finder.get())
    def setupWindows(self):
        self.plot = StringVar(None,self.model.getMethod().get_plot())
        self.windows.grid_rowconfigure(0, weight=1)
        self.windows.grid_rowconfigure(1,weight=2)
        self.windows.grid_rowconfigure(2, weight=1)  # Ajout d'une ligne pour les boutons
        self.windows.grid_columnconfigure(0, weight=1)
        
        frameStrategy = ttk.Frame(self.windows)
        frameStrategy.grid(column=0, row=0, sticky="ew")
        frameStrategy.grid_columnconfigure(0, weight=1)
        frameStrategy.grid_columnconfigure(1, weight=1)
        frameStrategy.grid_columnconfigure(2, weight=1)
        
        strategiesLabel = Label(frameStrategy, text="Strategy")
        strategiesLabel.grid(column=1, row=0, sticky="ew", pady=20)
        
        #birectangleAnalogy
        birect_analogy_combo = ttk.Combobox(
            frameStrategy, 
            values=list(self.birectangleAnalogyStrategy.keys()), 
            state="readonly"
        )
        birect_analogy_combo.set(
            list(self.birectangleAnalogyStrategy.keys())[
                list(self.birectangleAnalogyStrategy.values()).index(
                    self.model.getMethod().getBirectangleAnalogy().__class__
                )
            ]
        )
        birect_analogy_combo.grid(column=0, row=2, sticky="ew")
        labelBirectangle = Label(frameStrategy, text="Birectangle analogy")
        labelBirectangle.grid(column=0, row=1, sticky="ew")
        
        #cuttingMethod
        cuttingLabel = Label(frameStrategy,text="Cutting method")
        birect_cutting_combo = ttk.Combobox(frameStrategy,values=list(self.cuttingStrategy.keys()),state="readonly")
        birect_cutting_combo.set(list(self.cuttingStrategy.keys())[
                list(self.cuttingStrategy.values()).index(
                    self.model.getMethod().getCuttingMethod().__class__
                )
            ])
        birect_cutting_combo.grid(column=1,row=2)
        cuttingLabel.grid(column=1,row=1)
        
        
        #innerRectangleFinderMethod
        innerRectangleLabel = Label(frameStrategy,text="Inner rectangle finder method")
        inner_rectangle_finder_combo = ttk.Combobox(frameStrategy,values=list(self.innerRectangleFinderStrategy.keys()),state="readonly")
        inner_rectangle_finder_combo.set(list(self.innerRectangleFinderStrategy.keys())[
                list(self.innerRectangleFinderStrategy.values()).index(
                    self.model.getMethod().getInnerRectangleFinder().__class__
                )
            ])
        inner_rectangle_finder_combo.grid(column=2,row=2)
        innerRectangleLabel.grid(column=2,row=1)
        parametersFrame  = ttk.Frame(self.windows)
        parametersFrame.grid(column=0, row=1, sticky="ew")
        parametersFrame.grid_columnconfigure(0, weight=1)
        parametersFrame.grid_columnconfigure(1, weight=1)
        parametersFrame.grid_columnconfigure(2, weight=1)
      
        parameterLabel = Label(parametersFrame,text="parameters")
      
        epsilonLabel = Label(parametersFrame,text="epsilon")
        my_var= StringVar(parametersFrame)
        my_var.set(self.model.getMethod().getEpsilon())
        epsilonBox = Scale(parametersFrame, variable=my_var,from_=0.01, to=0.49,orient="horizontal",resolution=0.01)
      
        parameterLabel.grid(column=1,row=0,sticky="ew",pady=10)
        epsilonLabel.grid(column=0,row=0)
        epsilonBox.grid(column=0,row=1)

        #plot checkbox
        
        framePlotCheck  = ttk.Frame(parametersFrame)
        allStepCheckBox = Radiobutton(framePlotCheck,text="All step",variable=self.plot,value="step")
        lastStepCheckBox = Radiobutton(framePlotCheck,text="last step",variable=self.plot,value="last")
        noneStepCheckBox = Radiobutton(framePlotCheck,text="No step",variable=self.plot,value="none")
        rangeStepCheckBox = Radiobutton(framePlotCheck,text="Step only with detph < ",variable=self.plot,value="range")

        
        allStepCheckBox.select()
        vcmd = framePlotCheck.register(self.isDigit)
        entryRange = Entry(framePlotCheck,validate="all",validatecommand=(vcmd,'%P'))
        
        plotLabel = Label(framePlotCheck,text="plot")
        plotLabel.grid(column=1,row=0)
        
        allStepCheckBox.grid(column=0,row=1)
        lastStepCheckBox.grid(column=1,row=1)
        noneStepCheckBox.grid(column=2,row=1)
        rangeStepCheckBox.grid(column=3,row=1)
        entryRange.grid(column=4,row=1)
        
        framePlotCheck.grid(column=1,row=1)
        
        
         # Frame for OK and Cancel buttons
        frameButtons = ttk.Frame(self.windows)
        frameButtons.grid(column=0, row=2, sticky="ew", pady=10)
        frameButtons.grid_columnconfigure(0, weight=1)
        frameButtons.grid_columnconfigure(1, weight=0)  # Pas de poids pour la colonne centrale
        frameButtons.grid_columnconfigure(2, weight=1)
        
        cancelButton = Button(frameButtons, text="Annuler", command=self.on_cancel)
        okButton = Button(frameButtons, text="OK", command=self.on_ok)
        
        cancelButton.grid(column=1, row=0, sticky="e")
        okButton.grid(column=2, row=0, sticky="w")
        
    def on_cancel(self):
        # Logique pour le bouton Annuler
        self.hide()

    def on_ok(self):
        # Logique pour le bouton OK
        print("OK button pressed")
    def isDigit(self, digit):
        return str.isdigit(digit) or digit == "" and digit != "0"
class TomographyOption(ttk.Frame):
    def __init__(self, root,model:ShapeAnalogyModel):
        super().__init__(root)
        self.combo1 = ttk.Combobox(self, values=["Sub-option B1", "Sub-option B2"], state="readonly")
        self.combo1.set("Select a sub-option")
        self.combo2 = ttk.Combobox(self, values=["Sub-option B3", "Sub-option B4"], state="readonly")
        self.combo2.set("Select a sub-option")

    def show(self):
        self.pack(side="top")
        self.combo1.grid(column=0,row=0,pady= 10)
        self.combo2.grid(column=1,row=0,pady= 0)

    def hide(self):
        self.pack_forget()
        self.combo1.grid_forget()
        self.combo2.grid_forget()






class OptionView:
    model:ShapeAnalogyModel
    def __init__(self,root,model:ShapeAnalogyModel):
        self.model = model
        self.option_classes = {
            "bi-rectangle method": BiRectangleOption(root,model),
            "tomography method": TomographyOption(root,model)
        }
        frame = ttk.Frame(root)
        # Create the first select button (dropdown menu)
        self.combo = ttk.Combobox(frame, values=list(self.option_classes.keys()), state="readonly")
        self.combo.set("Select an option")
        self.combo.current(0)
        # Bind the selection event to the on_select function
        self.combo.bind("<<ComboboxSelected>>", self.on_select)
        # Initially hide all option classes
        for cls in self.option_classes.values():
            cls.hide()
            
        parametersPictureLabel = Button(frame,text="toto")
        
        parametersPicture = Image.open("resources/parametersPicture.png")
        image = ImageOps.contain(parametersPicture, (50,50), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        parametersPictureLabel.config(image=photo,command=self.on_click)
        parametersPictureLabel.image = photo
        
          # Place the combo box and the parameters picture label side by side
        self.combo.grid(column=0, row=0, padx=10)
        parametersPictureLabel.grid(column=1, row=0)
        frame.pack(side="top",pady=10)
        parametersPictureLabel.bind("<<")
    def on_select(self,event):
        for opt in self.option_classes.values():
            opt.hide()
        selected_option = self.combo.get()
        self.model.change_method(selected_option)
    def on_click(self):
        selected_option = self.combo.get()
        current_class = self.option_classes.get(selected_option)
        if not current_class.is_open():
            current_class.show()
        