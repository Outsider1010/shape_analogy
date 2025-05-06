from tkinter import ttk,Toplevel,Label,Button,Spinbox,StringVar,Radiobutton,Entry,Scale,IntVar,messagebox,Checkbutton,BooleanVar,DoubleVar
from src.ShapeAnalogyModel import ShapeAnalogyModel
from PIL import Image, ImageTk,ImageTk,ImageOps
from src.birectangle.cuttingmethod.cut_in_8 import CuttingIn8

from src.birectangle.rectangleanalogy.center_dim_analogy import CenterDimAnalogy
from src.birectangle.rectangleanalogy.top_left_dim_analogy import TopLeftDimAnalogy
from src.birectangle.birectangleanalogy.ext_sigmoid_analogy import ExtSigmoidAnalogy
from src.birectangle.rectangleanalogy.area_analogy import AreaAnalogy
from src.birectangle.rectangleanalogy.coord_analogy import CoordAnalogy
from src.birectangle.innerrectanglefinder.barycenter_rectangle_finder import BarycenterRectangleFinder
from src.birectangle.cuttingmethod.cut_in_4_equal_parts_1 import CutIn4EqualParts1
from src.birectangle.birectangleanalogy.simple_analogy import SimpleAnalogy
from src.birectangle.cuttingmethod.horizontal_cut import HorizontalCut
from src.birectangle.cuttingmethod.vertical_cut import VerticalCut
from src.birectangle.cuttingmethod.sides_non_disjoint_cut import SidesNonDisjointCut
from src.birectangle.innerrectanglefinder.largest_rectangle_finder import LargestRectangleFinder
from src.birectangle.birectangleanalogy.bi_segment_analogy import BiSegmentAnalogy
from src.birectangle.overflowprevention.direct_prevention import DirectPrevention
from src.birectangle.overflowprevention.indirect_prevention import IndirectPrevention
from src.birectangle.overflowprevention.no_prevention import NoPrevention


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
            "Barycenter method": BarycenterRectangleFinder
        }
    
        self.rectangleAnalogyStrategy = {
            "Center dimension analogy": CenterDimAnalogy,
            "Top left dimension analogy": TopLeftDimAnalogy,
            "Coords Analogy":CoordAnalogy,
            "Area Analogy":AreaAnalogy
        }
        
        self.overflowPreventionStrategy = {
            "Direct prevention":DirectPrevention,
            "Indirect prevention":IndirectPrevention,
            "No prevention":NoPrevention,
        }
        self.rectangleAnalogy = CenterDimAnalogy
    def show(self):
        if not self.is_window_open():
            self.windows = Toplevel(self.root)
            self.setup_windows()

    def is_window_open(self):
        return self.windows is not None and self.windows.winfo_exists()

    def hide(self):
        if(self.windows):
            self.windows.destroy()   
   
    def setup_windows(self):
        self.windows.title("Parameters")
        self.windows.grid_rowconfigure(1, weight=1)
        self.windows.grid_columnconfigure(0, weight=1)
        self.windows.grid_rowconfigure(0, weight=1)
        
        # Strategy Frame
        strategy_frame = ttk.Frame(self.windows)
        strategy_frame.grid(column=0, row=0, sticky="nsew", padx=10, pady=10)
        
        for i in range(5):
            strategy_frame.grid_columnconfigure(i, weight=1)
        
        Label(strategy_frame, text="Strategy").grid(column=0, row=0, columnspan=4, pady=10, sticky="ew")
        
        Label(strategy_frame, text="Birectangle analogy").grid(column=0, row=1, sticky="ew")
        self.birect_analogy_combo = ttk.Combobox(strategy_frame, values=list(self.birectangleAnalogyStrategy.keys()), state="readonly")
        self.birect_analogy_combo.set(
            list(self.birectangleAnalogyStrategy.keys())[
                list(self.birectangleAnalogyStrategy.values()).index(
                    self.model.getMethod().getBirectangleAnalogy().__class__
                )
            ]
        )
        self.birect_analogy_combo.grid(column=0, row=2, padx=5, sticky="ew")
        
        Label(strategy_frame, text="Cutting Method").grid(column=1, row=1, sticky="ew")
        self.birect_cutting_combo = ttk.Combobox(strategy_frame, values=list(self.cuttingStrategy.keys()), state="readonly")
        self.birect_cutting_combo.set(list(self.cuttingStrategy.keys())[
                list(self.cuttingStrategy.values()).index(
                    self.model.getMethod().getCuttingMethod().__class__
                )
            ])
        self.birect_cutting_combo.grid(column=1, row=2, padx=5, sticky="ew")
        
        Label(strategy_frame, text="Inner rectangle finder method").grid(column=2, row=1, sticky="ew")
        self.inner_rectangle_finder_combo = ttk.Combobox(strategy_frame, values=list(self.innerRectangleFinderStrategy.keys()), state="readonly")
        self.inner_rectangle_finder_combo.set(list(self.innerRectangleFinderStrategy.keys())[
                list(self.innerRectangleFinderStrategy.values()).index(
                    self.model.getMethod().getInnerRectangleFinder().__class__
                )
            ])
        self.inner_rectangle_finder_combo.grid(column=2, row=2, padx=5, sticky="ew")
        
        Label(strategy_frame, text="Rectangle analogy").grid(column=3, row=1, sticky="ew")
        self.rectangleAnalogy_combo = ttk.Combobox(strategy_frame, values=list(self.rectangleAnalogyStrategy.keys()), state="readonly")
        self.rectangleAnalogy_combo.set(
             list(self.rectangleAnalogyStrategy.keys())[
                list(self.rectangleAnalogyStrategy.values()).index(
                    self.rectangleAnalogy
                )
            ]
        )
        self.rectangleAnalogy_combo.grid(column=3, row=2, padx=5, sticky="ew")

        Label(strategy_frame, text="Overflow prevention").grid(column=4, row=1, sticky="ew")
        self.overflowPreventionComboBox = ttk.Combobox(strategy_frame, values=list(self.overflowPreventionStrategy.keys()), state="readonly")
        self.overflowPreventionComboBox.set(
            list(self.overflowPreventionStrategy.keys())[
                list(self.overflowPreventionStrategy.values()).index(
                    self.model.getMethod().getOverflowPrevention().__class__
                )
            ]
        )
        self.overflowPreventionComboBox.grid(column=4, row=2, padx=5, sticky="ew")
        
        
        parameters_frame = ttk.Frame(self.windows)
        parameters_frame.grid(column=0, row=1, sticky="nsew", padx=10, pady=10)

        
        for i in range(3):
            parameters_frame.grid_columnconfigure(i, weight=1)
        
        Label(parameters_frame, text="Parameters").grid(column=0, row=0, columnspan=4, pady=10, sticky="ew")
        
        Label(parameters_frame, text="Epsilon").grid(column=0, row=1, sticky="ew",pady=10)
        self.epsilon = DoubleVar(parameters_frame, self.model.getMethod().getEpsilon())
        epsilon_frame = ttk.Frame(parameters_frame)
        Scale(epsilon_frame, from_=0.000001, to=0.49, orient="horizontal", resolution=0.000001,variable=self.epsilon,showvalue=0,command=lambda value: self.epsilonLabel.config(text=f"{value}")).grid(column=0, row=0, padx=5, sticky="ew")
        self.epsilonLabel = Label(epsilon_frame,text=f"{self.epsilon.get()}")
        self.epsilonLabel.grid(column=0,row=1)
        epsilon_frame.grid(column=0,row=2,padx=5, sticky="ew")
        
       
        plot_frame = ttk.Frame(parameters_frame)
        self.stepRangeVariable = StringVar()
        default_plot = self.model.getMethod().getPlottingBehavior()
        if(isinstance(default_plot, int)):
            self.stepRangeVariable.set(default_plot)
            default_plot = "range"
        
        self.plot = StringVar(master=plot_frame,value=default_plot)
        plot_frame.grid(column=1, row=2, rowspan=5, sticky="ew")
        allStepCheckBox = Radiobutton(plot_frame, text="All Step", variable=self.plot, value="step")
        lastStepCheckBox = Radiobutton(plot_frame, text="last step", variable=self.plot, value="last")
        noneStepCheckBox = Radiobutton(plot_frame, text="No Step", variable=self.plot, value="none")
        rangeStepCheckBox = Radiobutton(plot_frame, text="Step only with depth <", variable=self.plot, value="range")
        
        
        vcmd = plot_frame.register(self.isDigit)
        self.stepRange = Entry(plot_frame, validate="all", validatecommand=(vcmd, '%P'),textvariable=self.stepRangeVariable)
        
        plotLabel = Label(plot_frame, text="plot")
        plotLabel.grid(column=1, row=0)
        
        allStepCheckBox.grid(column=0, row=1)
        lastStepCheckBox.grid(column=1, row=1)
        noneStepCheckBox.grid(column=2, row=1)
        rangeStepCheckBox.grid(column=3, row=1)
        self.stepRange.grid(column=4, row=1)
        
        plot_frame.grid(column=1, row=1)
        
        Label(parameters_frame, text="choice of next Rx").grid(column=2, row=1, sticky="ew",pady=10)
        self.subSys = StringVar(None, self.model.getMethod().getSubSys() if self.model.getMethod().getSubSys() != '' else 'first')
        choice_frame = ttk.Frame(parameters_frame)
        cutSubSysCheck = Radiobutton(choice_frame, text="Cutting rectangle", variable=self.subSys, value="cut")
        firstSubSysCheck = Radiobutton(choice_frame, text="first Rx", variable=self.subSys, value="first")
        superSubSysCheck = Radiobutton(choice_frame, text="Rx of super shape",variable=self.subSys, value="super")
        cutSubSysCheck.grid(column=0, row=0, sticky="w")
        firstSubSysCheck.grid(column=1, row=0, sticky="w")
        superSubSysCheck.grid(column=2, row=0, sticky="w")
        choice_frame.grid(column=2, row=1, rowspan=3, sticky="ew")
        
        secondParametersFrame = ttk.Frame(self.windows)
        sameAxisFrame = ttk.Frame(secondParametersFrame)
        self.sameAxisVariable = BooleanVar(sameAxisFrame,self.model.getMethod().getSameAxis())
        sameAxisLabel = Label(sameAxisFrame,text="SameAxis")
        sameAxisCheckBoutton = Checkbutton(sameAxisFrame,variable=self.sameAxisVariable)
        sameAxisCheckBoutton.grid(column=0,row=1,pady=10)
        sameAxisLabel.grid(column=0,row=0)
        sameAxisFrame.grid(column=0,row=0)
        secondParametersFrame.grid(column=0,row=2,sticky="nsew",pady=10,padx=10)
        
        
        ratioFrame = ttk.Frame(secondParametersFrame)
        self.ratioVariable = BooleanVar(ratioFrame,self.model.getMethod().getRatio())
        ratioLabel = Label(ratioFrame,text="Ratio")
        ratioCheckBoutton = Checkbutton(ratioFrame,variable=self.ratioVariable)
        ratioCheckBoutton.grid(column=0,row=1,pady=10)
        ratioLabel.grid(column=0,row=0)
        ratioFrame.grid(column=1,row=0)
        
        innerReductionFrame = ttk.Frame(secondParametersFrame)
        self.innerReductionVariable = BooleanVar(innerReductionFrame,self.model.getMethod().getInnerReduction())
        innerReductionLabel = Label(innerReductionFrame,text="InnerReduction")
        innerReductionCheckBoutton = Checkbutton(innerReductionFrame,variable=self.innerReductionVariable)
        innerReductionCheckBoutton.grid(column=0,row=1,pady=10)
        innerReductionLabel.grid(column=0,row=0)
        innerReductionFrame.grid(column=2,row=0)
        
        algoModFrame = ttk.Frame(secondParametersFrame)
        algoModLabel = Label(algoModFrame,text="algorithme iteration",anchor="center")
        self.algoModVariable = StringVar(algoModFrame,self.model.getMethod().getAlgo())
        
        iterRadio = Radiobutton(algoModFrame,text="Iterative",value="iter",variable=self.algoModVariable)
        recRadio = Radiobutton(algoModFrame,text="Recursive",value="rec",variable=self.algoModVariable)
        iterRadio.grid(column=0,row=1,padx=10)
        recRadio.grid(column=1,row=1)
        algoModLabel.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        algoModFrame.grid_columnconfigure(1, weight=1)
        algoModFrame.grid_columnconfigure(0, weight=1)
        algoModFrame.grid(row=0,column=3,sticky="n")
        
        nbIterationsFrame = ttk.Frame(secondParametersFrame)
        nbIterationsLabel = Label(nbIterationsFrame,text="maximum of iterations")
        vcmd = nbIterationsFrame.register(self.isDigit)
        self.nbIterationVariable = IntVar(nbIterationsFrame,self.model.getMethod().getNbIteration())
        nbIterationsSpin = Spinbox(nbIterationsFrame,from_=1,to=10000000000000000,validate="key", validatecommand=(vcmd, '%P'),textvariable=self.nbIterationVariable)
        nbIterationsLabel.grid(column=0,row=0)
        nbIterationsSpin.grid(column=0,row=1,pady=(10,0))
        nbIterationsFrame.grid(row=0,column=4)
        
        maxDepthFrame = ttk.Frame(secondParametersFrame)
        maxDepthLabel = Label(maxDepthFrame,text="maximum of depths")
        vcmd = maxDepthFrame.register(self.isDigit)
        self.maxDepthVariable = IntVar(nbIterationsFrame,self.model.getMethod().get_maxDepth())
        maxDepthSpin = Spinbox(maxDepthFrame,from_=1,to=10000000000000000,validate="key", validatecommand=(vcmd, '%P'),textvariable=self.maxDepthVariable)
        maxDepthLabel.grid(column=0,row=0)
        maxDepthSpin.grid(column=0,row=1,pady=(10,0))
        maxDepthFrame.grid(row=0,column=5)
        # Buttons Frame
        buttons_frame = ttk.Frame(self.windows)
        buttons_frame.grid(column=0, row=3, pady=10, sticky="ew")
        self.windows.grid_rowconfigure(2, weight=1)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=0)
        buttons_frame.grid_columnconfigure(2, weight=0)
        buttons_frame.grid_columnconfigure(3, weight=1)
        
        cancelButton = Button(buttons_frame, text="Cancel", command=self.on_cancel)
        okButton = Button(buttons_frame, text="OK", command=self.on_ok)
        
        cancelButton.grid(column=2, row=0)
        okButton.grid(column=1, row=0)
        
    def on_cancel(self):
        # Logique pour le bouton Annuler
        self.hide()

    def on_ok(self):
        method = self.model.getMethod()
        nbIteration = self.nbIterationVariable.get()
        innerReduction = self.innerReductionVariable.get()
        ratio = self.ratioVariable.get()
        maxDepth = self.maxDepthVariable.get()
        preventionMethod = self.overflowPreventionStrategy[self.overflowPreventionComboBox.get()]
        birectangleAnalogyMethod = self.birectangleAnalogyStrategy[self.birect_analogy_combo.get()]
        if(ratio and not innerReduction):
            self.showError("To enable ratio you have enable innerReduction")
            return
        if(nbIteration == ""):
            self.showError("Number of iterations must be indicate")
            return
        if(maxDepth == ""):
            self.showError("Maximum depth must be indicate")
            return
        
        if(self.plot.get() == "range"):
            if(self.stepRange.get() == ""):
                self.showError("You have selected step only with depth < at some numbers, pls indicate the step index you want")
                return
            else:
                method.setPlottingBehavior(int(self.stepRangeVariable.get()))
        else:
            method.setPlottingBehavior(self.plot.get())
        method.setEpsilon(self.epsilon.get())
        method.setSubSys(self.subSys.get())
        self.rectangleAnalogy = self.rectangleAnalogyStrategy[self.rectangleAnalogy_combo.get()]
        method.set_birectangle_analogy_method(birectangleAnalogyMethod(self.rectangleAnalogy()))
        method.setCuttingMethod(self.cuttingStrategy[self.birect_cutting_combo.get()]())
        method.setInnerRectangleFinder(self.innerRectangleFinderStrategy[self.inner_rectangle_finder_combo.get()]())
        method.setOverflowPrevention(preventionMethod(self.epsilon.get(),birectangleAnalogyMethod()) if preventionMethod == self.overflowPreventionStrategy["Indirect prevention"] else preventionMethod())
        method.setSameAxis(self.sameAxisVariable.get())
        method.setInnerReduction(innerReduction)
        method.setRatio(self.ratioVariable.get())
        method.setAlgo(self.algoModVariable.get())
        method.setNbIteration(self.nbIterationVariable.get()) 
        method.set_maxDepth(self.maxDepthVariable.get())
        self.hide()
        
    def isDigit(self, digit):
        return ((str.isdigit(digit) and "." not in digit) or digit == "") and digit != "0"
    def showError(self,message):
        messagebox.showerror("Error",message=message,parent = self.windows)
        pass
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
            "bi-rectangle method": BiRectangleOption(root,model)
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
        if not current_class.is_window_open():
            current_class.show()
        