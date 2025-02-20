from tkinter import ttk



class StrategyView(ttk.Frame):
    def __init__(self, parent):
      super().__init__(parent)
      self.place(relx=0,rely=0,relheight=1,width=150)
      self.configure(relief='solid',borderwidth =2)
      