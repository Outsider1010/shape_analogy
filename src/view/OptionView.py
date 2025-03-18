from tkinter import ttk,Toplevel,Label,Button,Spinbox,StringVar,Radiobutton
from src.ShapeAnalogyModel import ShapeAnalogyModel
from PIL import Image, ImageTk,ImageTk,ImageOps
from src.birectangle.cuttingmethod.CuttingIn8Method import CuttingIn8Method
from src.birectangle.pointanalogy.ArithmeticPointAnalogy import ArithmeticPointAnalogy
from src.birectangle.rectangleanalogy.CenterDimAnalogy import CenterDimAnalogy
from src.birectangle.rectangleanalogy.TopLeftDimAnalogy import TopLeftDimAnalogy
from src.birectangle.birectangleanalogy.SigmoidCenterAnalogy import SigmoidCenterAnalogy
from src.birectangle.birectangleanalogy.ExtSigmoidAnalogy import ExtSigmoidAnalogy
from src.birectangle.birectangleanalogy.SigmoidCenterAnalogy import SigmoidCenterAnalogy
from src.birectangle.birectangleanalogy.ExtSigmoidAnalogy import ExtSigmoidAnalogy
from src.birectangle.cuttingmethod.FirstCuttingIn4Method import FirstCuttingIn4Method
from src.birectangle.birectangleanalogy.CornerSigmoidAnalogy import CornerAnalogy
from src.birectangle.cuttingmethod.FullHorizontalCut import FullHorizontalCut
from src.birectangle.cuttingmethod.FullVerticalCut import FullVerticalCut
from src.birectangle.cuttingmethod.FullSideNonDisjointCut import FullSideNonDisjointCut
from src.birectangle.innerrectanglefinder.LargestRectangleFinder import LargestRectangleFinder
from src.birectangle.birectangleanalogy.BiSegmentAnalogy import BiSegmentAnalogy
# Define the classes representing the options
class BiRectangleOption():

    def __init__(self,root,model:ShapeAnalogyModel):
        self.model = model
        self.root = root
        self.windows = None
        self.birectangleAnalogyStrategy = {
            "Sigmoid center":SigmoidCenterAnalogy,
            "Extended sigmoid":ExtSigmoidAnalogy,
            "BiSegment Analogy":BiSegmentAnalogy,
            "CornerSigmoidAnalogy":CornerAnalogy
        }
        self.cuttingStrategy = {
            "Cut4":FirstCuttingIn4Method,
            "Cut8":CuttingIn8Method,
            "Horizontal cut":FullHorizontalCut,
            "Vertical cut": FullVerticalCut,
            "Non disjoint cut":FullSideNonDisjointCut,
            
        }
        self.innerRectangleFinderStrategy = {
            "Largest rectangle": LargestRectangleFinder,
        }
        self.pointAnalogyStrategy = {
            "Arithmetic analogy": ArithmeticPointAnalogy,
        }
        self.rectangleAnalogyStrategy = {
            "Center dimension analogy": CenterDimAnalogy,
            "Top left dimension analogy": TopLeftDimAnalogy,
        }
        
        """self.birect_cutting_combo = ttk.Combobox(self,values=self.model.get_birectangle_cutting_strategy(),state="readonly")
        self.birect_cutting_combo.set(self.model.get_birectangle_cutting_strategy_values())
        self.birect_inner_rectangle_finder = ttk.Combobox(self,values=self.model.get_birectangle_inner_rectangle_finder_strategy(),state="readonly")
        self.birect_inner_rectangle_finder.set(self.model.get_birectangle_inner_rectangle_finder_strategy_values())
        self.birect_analogy_combo.bind("<<ComboboxSelected>>",self.select_analogy_strategy)
        self.birect_cutting_combo.bind("<<ComboboxSelected>>",self.select_cutting_strategy)
        self.birect_inner_rectangle_finder.bind("<<ComboboxSelected>>",self.select_inner_rectangle_finder_strategy)"""

    def show(self):
        self.windows = Toplevel(self.root)
        self.setupWindows()

    """self.birect_inner_rectangle_finder.grid(column=2,row=0)
        self.birect_cutting_combo.grid(column=1,row=0,padx=20)
        self.birect_analogy_combo.grid(column=0,row=0,padx=20)"""
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
        plot = StringVar()
        self.windows.grid_rowconfigure(0, weight=1)
        self.windows.grid_rowconfigure(1,weight=2)
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
        #Set the default value for SpinBox
        my_var= StringVar(parametersFrame)
        my_var.set(self.model.getMethod().getEpsilon())
        epsilonBox = Spinbox(parametersFrame, from_=0.01, to=0.45,increment=0.05,textvariable=my_var)
      
        parameterLabel.grid(column=1,row=0,sticky="ew")
        epsilonLabel.grid(column=0,row=0)
        epsilonBox.grid(column=0,row=1)

        #plot checkbox
        framePlotCheck  = ttk.Frame(parametersFrame)
        allStepCheckBox = Radiobutton(framePlotCheck,text="All step",variable=plot,value="step")
        lastStepCheckBox = Radiobutton(framePlotCheck,text="last step",variable=plot,value="last")
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
        