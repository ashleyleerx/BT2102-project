from tkinter import Toplevel, Label, Button, StringVar, Entry, Tk


class PaymentStatement(Toplevel): 
    def __init__(self, master): 
        Toplevel.__init__(self,master)
        self.title("Payment Confirmation")
        self.geometry
        ("800x600") 
        Label(self, text="Thanks for paying the Fine of").pack()
        Label(self, text="$[total_fine]").pack()
        Label(self, text="You may now continue to").pack()
        Label(self, text="borrow/reserve more books").pack()
        Button(self, text="OK", command = self.check_login).pack()
        
        
    def check_login(self):
        self.master.overlay()
        self.after(2000,self.destroy)


