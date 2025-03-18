from tkinter import ttk,Toplevel,Label,Button
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
from src.birectangle.innerrectanglefinder.InnerRectangleFinder import InnerRectangleFinder
from src.birectangle.innerrectanglefinder.LargestRectangleFinder import LargestRectangleFinder
# Define the classes representing the options
class BiRectangleOption(ttk.Frame):

    def __init__(self,root,model:ShapeAnalogyModel):
        super().__init__(root)
        self.model = model
        self.root = root
        self.windows = None
        self.birectangleAnalogyStrategy = {
            "Sigmoid center":SigmoidCenterAnalogy(),
            "Extended sigmoid":ExtSigmoidAnalogy(),
            "BiSegment Analogy":BiSegmentAnalogy(),
            "CornerSigmoidAnalogy":CornerAnalogy()
        }
        self.cuttingStrategy = {
            "Cut4":FirstCuttingIn4Method(),
            "Cut8":CuttingIn8Method(),
            "Horizontal cut":FullHorizontalCut(),
            "Vertical cut": FullVerticalCut(),
            "Non disjoint cut":FullSideNonDisjointCut(),
            
        }
        self.innerRectangleFinderStrategy = {
            "Largest rectangle": LargestRectangleFinder()
        }
        self.pointAnalogyStraty = {
            "Arithmetic analogy": ArithmeticPointAnalogy()
        }
        self.rectangleAnalogy = {
            "Center dimension analogy": CenterDimAnalogy(),
            "Top left dimension analogy": TopLeftDimAnalogy()
        }
        self.birect_analogy_combo = ttk.Combobox(self, values=self.birectangleAnalogyStrategy, state="readonly")
        self.birect_analogy_combo.set()
        """self.birect_cutting_combo = ttk.Combobox(self,values=self.model.get_birectangle_cutting_strategy(),state="readonly")
        self.birect_cutting_combo.set(self.model.get_birectangle_cutting_strategy_values())
        self.birect_inner_rectangle_finder = ttk.Combobox(self,values=self.model.get_birectangle_inner_rectangle_finder_strategy(),state="readonly")
        self.birect_inner_rectangle_finder.set(self.model.get_birectangle_inner_rectangle_finder_strategy_values())
        self.birect_analogy_combo.bind("<<ComboboxSelected>>",self.select_analogy_strategy)
        self.birect_cutting_combo.bind("<<ComboboxSelected>>",self.select_cutting_strategy)
        self.birect_inner_rectangle_finder.bind("<<ComboboxSelected>>",self.select_inner_rectangle_finder_strategy)"""

    def show(self):
        self.windows = Toplevel(self.root)
        self.pack(side="top")
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
        