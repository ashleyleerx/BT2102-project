import tkinter as tk

from payment_statement import *

    
class NewPaymentWindow(tk.Frame): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        Label(master=self, text="Welcome User",width=20,height=2).pack()

        # #top frame
        # top_frame = tk.Frame(master=self, width = 00, height = 50, bg = "grey60")
        # top_frame.pack()

        # for r in range(8):
        #     top_frame.rowconfigure(r, weight=1)

        # for c in range(10):
        #     top_frame.columnconfigure(c, weight=1)
        # Label(top_frame, text="Welcome User",width=20,height=2).grid(row=3,column=9)
        
        # #middle frame
        # middle_frame = tk.Frame(master=self, width = 800, height = 700, bg = "grey60")
        # middle_frame.pack(padx=20, pady=25)
        
        
        # #bottom frame
        # bottom_frame = tk.Frame(master=self, width =800, height = 450)
        # bottom_frame.pack

        # for r in range(8):
        #     bottom_frame.rowconfigure(r, weight=1)

        # for c in range(10):
        #     bottom_frame.columnconfigure(c, weight=1)
        # fine_button = Button(bottom_frame, text="Pay Fines",width=20,height=4)
        # fine_button.bind("<Button>", lambda e : PaymentStatement(self))
        # fine_button.grid(row=4,column=3)   
        # Button(bottom_frame, text="Cancel",width=20,height=4).grid(row=4,column=6)
        
            
root = tk.Tk()
root.geometry('400x400')
myapp = NewPaymentWindow(root)
myapp.pack()
root.mainloop()