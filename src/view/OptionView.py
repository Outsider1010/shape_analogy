from tkinter import ttk
from src.ShapeAnalogyModel import ShapeAnalogyModel

# Define the classes representing the options
class BiRectangleOption(ttk.Frame):

    def __init__(self,root,model:ShapeAnalogyModel):
        super().__init__(root)
        self.model = model
        self.birect_analogy_combo = ttk.Combobox(self, values=self.model.get_birectangle_birectangleAnalogy_strategy(), state="readonly")
        self.birect_analogy_combo.set(self.model.get_birectangle_birectangleAnalogy_strategy_values())
        self.birect_cutting_combo = ttk.Combobox(self,values=self.model.get_birectangle_cutting_strategy(),state="readonly")
        self.birect_cutting_combo.set(self.model.get_birectangle_cutting_strategy_values())
        self.birect_inner_rectangle_finder = ttk.Combobox(self,values=self.model.get_birectangle_inner_rectangle_finder_strategy(),state="readonly")
        self.birect_inner_rectangle_finder.set(self.model.get_birectangle_inner_rectangle_finder_strategy_values())
        self.birect_analogy_combo.bind("<<ComboboxSelected>>",self.select_analogy_strategy)
        self.birect_cutting_combo.bind("<<ComboboxSelected>>",self.select_cutting_strategy)
        self.birect_inner_rectangle_finder.bind("<<ComboboxSelected>>",self.select_inner_rectangle_finder_strategy)

    def show(self):
        self.pack(side="top")
        self.birect_inner_rectangle_finder.grid(column=2,row=0)
        self.birect_cutting_combo.grid(column=1,row=0,padx=20)
        self.birect_analogy_combo.grid(column=0,row=0,padx=20)

    def hide(self):
        self.pack_forget()
        self.birect_inner_rectangle_finder.grid_forget()
        self.birect_cutting_combo.grid_forget()
        self.birect_analogy_combo.grid_forget()
        
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
        # Create the first select button (dropdown menu)
        self.combo = ttk.Combobox(root, values=list(self.option_classes.keys()), state="readonly")
        self.combo.set("Select an option")
        self.combo.pack(side="top",pady=10)
        self.combo.current(0)
        # Bind the selection event to the on_select function
        self.combo.bind("<<ComboboxSelected>>", self.on_select)
        # Initially hide all option classes
        for cls in self.option_classes.values():
            cls.hide()
        self.option_classes[self.combo.get()].show()
        
    def on_select(self,event):
        for opt in self.option_classes.values():
            opt.hide()
        selected_option = self.combo.get()
        self.model.change_method(selected_option)
        current_class = self.option_classes.get(selected_option)
        current_class.show()