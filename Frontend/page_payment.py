import tkinter as tk
from tkinter import messagebox

import GetViews as gv
import FP_Manager as fm
    
class PaymentPage(tk.Frame): 
    def __init__(self, parent, controller, session_user_data):
        super().__init__(parent)
        self.parent, self.controller = parent, controller
        #controller.option_add('*Dialog.msg.font', 'Helvetica 24')
        
        ## Session variables ##
        self.user_data = session_user_data
        self.user_name = self.user_data["userId"]
        
        ## For user fines ##
        self.user_fines = tk.DoubleVar()
        self.get_fines()

        ## Initialize widgets ##
        self.create_widgets()
        
    def get_fines(self):
        #Get total fines
        total_fines = gv.member_view_totalfineamount(self.user_name)
        self.user_fines.set(total_fines)
        self.user_data["unpaid_fines"] = True if total_fines > 0 else False
        
    def create_widgets(self):
        ## Main frame ##
        main_frame= tk.Frame(master=self, width = 200, height=300)
        main_frame.pack(fill=tk.BOTH, padx=20, pady=(10,20),expand=True)
        
        main_frame.rowconfigure(0, weight=7)
        main_frame.rowconfigure(1, weight=3)
        main_frame.columnconfigure(0, weight=1)
            
        #Payment screen    
        payment_screen = tk.Frame(master=main_frame)
        payment_screen.grid(row=0,column=0,sticky="nsew")
        df = gv.member_view_unpaidfines(self.user_name)
        self.fill_payment(df, payment_screen)
        
        #Create Buttons
        frm_bottom = tk.Frame(master=main_frame)
        frm_bottom.grid(row=1,column=0,sticky="nsew")
        
        frm_btns = tk.Frame(master=frm_bottom)
        frm_btns.pack(pady=30)
        pay_button = tk.Button(master=frm_btns, text="Pay Fines",
                               bg="lightblue",activebackground="lightblue",
                               width=20,height=3,font=('', 10),
                               command = self.on_pay_fine_button_press)
        pay_button.pack(side=tk.LEFT,padx=30)
        
        cancel_button = tk.Button(master=frm_btns, text="Cancel",
                                  bg ="LightCoral",activebackground="LightCoral",
                                  width=20,height=3,font=('', 10),
                                  command = self.on_cancel_button_press)
        cancel_button.pack(side=tk.LEFT,padx=30)
                
    def fill_payment(self, df, frame):
        frm_fines = tk.Frame(master=frame, bg="white", borderwidth=1,relief=tk.GROOVE)
        frm_fines.pack(side=tk.TOP)
        ## Fines Table ##
        frm_fines_table = tk.Frame(master=frm_fines, bg = "white")
        frm_fines_table.pack(pady=(10,20),padx=40)
        #Two columns
        for c in range(2):
            frm_fines_table.columnconfigure(c, weight=1)
        #Headers
        lbl_date = tk.Label(master=frm_fines_table,text="Date", 
                             width = 10, font=('', 15,"bold"),bg = "white")
        lbl_date.grid(row=0,column=0,padx=20,pady=7)
        lbl_amt = tk.Label(master=frm_fines_table,text="Amount", 
                            width = 10, font=('', 15,"bold"),bg = "white")
        lbl_amt.grid(row=0,column=1,padx=20,pady=7)
        #Making individual rows - Assume: index < 4 
        for index, row in df.iterrows():
            print(index)
            #Book data
            lbl_date = tk.Label(master=frm_fines_table,text=row[0],
                                 width = 10, font=('', 15),bg = "white")
            lbl_date.grid(row=index+1,column=0,padx=10,pady=7)
            
            lbl_amt = tk.Label(master=frm_fines_table,text="$" + str(row[1]) + ".00",
                                width = 10, font=('', 15),bg = "white")
            lbl_amt.grid(row=index+1,column=1,padx=10,pady=7)
            
        total_label = tk.Label(master=frm_fines, 
                               text = "Total Fine: $" + str(self.user_fines.get()),
                               bg = "white",foreground="red", font=('', 20))
        total_label.pack()
        
    ## UI Event Helpers ##
    def on_cancel_button_press(self):
        self.destroy()   
        
    def on_pay_fine_button_press(self):
        if not self.user_data["unpaid_fines"]: 
            tk.messagebox.showinfo("Payment","You do not have any outstanding fines.")
        elif not fm.returned_overduebks(self.user_name):
            msg = "Please return all overdue books before making payment."
            tk.messagebox.showerror("Payment",msg)
        else:
            fm.make_payment(self.user_name)
            borrow_cfm_msg = "Thank you for paying your fine"
            borrow_cfm_msg += "\nYou may now continue to borrow/reserve more books"
            tk.messagebox.showinfo("Payment Confirmation",borrow_cfm_msg)
            self.destroy()
            self.controller.refresh_home()
        
# root = tk.Tk()

# root.geometry('600x600')
# root.minsize(600,600)
# container = tk.Frame(root)
# container.pack(side = "top", fill = "both", expand = True) 
# container.grid_rowconfigure(0, weight = 1)
# container.grid_columnconfigure(0, weight = 1)

# test_user = {"userId":"willywonka69"}

# frame = PaymentPage(container,root,test_user)
# frame.grid(row = 0, column = 0, sticky ="nsew")
# frame.tkraise()
# root.mainloop()  