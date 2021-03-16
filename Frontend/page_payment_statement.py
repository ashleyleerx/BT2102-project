import tkinter as tk


class PaymentStatement(tk.Frame): 
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent, self.controller = parent, controller
        self.create_widgets()
        for r in range(20):
            self.rowconfigure(r, weight=1)
            
        for c in range(3):
            self.columnconfigure(c, weight=1)
            
    def create_widgets(self):
        tk.Label(self, text="Thanks for paying", font=('', 15)).grid(row=8,column=1)
        tk.Label(self, text="your fine", font=('', 15)).grid(row=9,column=1)
        tk.Label(self, text="You may now continue to", font=('', 15)).grid(row=10,column=1)
        tk.Label(self, text="borrow/reserve more books", font=('', 15)).grid(row=11,column=1)
        ok_button = tk.Button(self, text="OK", font=('', 15), command = lambda :self.controller.show_frame(self.controller.PAGES[1]))
        ok_button.grid(row=12,column=1)
        
        
        
root = tk.Tk()
root.geometry('600x600')
root.minsize(600,600)
container = tk.Frame(root)
container.pack(side = "top", fill = "both", expand = True) 
container.grid_rowconfigure(0, weight = 1)
container.grid_columnconfigure(0, weight = 1)
frame = PaymentStatement(container,root)
frame.grid(row = 0, column = 0, sticky ="nsew")
frame.tkraise()
root.mainloop()  
        



