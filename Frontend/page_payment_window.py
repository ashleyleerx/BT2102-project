import tkinter as tk

from header import create_header
import GetViews as gv
import FP_Manager as fm

HEADER_BG = "grey60"
    
class NewPaymentWindow(tk.Frame): 
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent, self.controller = parent, controller
        self.session_username = tk.StringVar()
        self.user_fines = tk.DoubleVar()
        # Get total fine
        self.user_fines.set(gv.member_view_totalfineamount(self.session_username.get()))
        
        ### DEVELOPMENT ONLY ###
        self.session_username.set("danielpo") 
        self.user_fines.set(gv.member_view_totalfineamount(self.session_username.get()))        
        self.create_widgets()
        


    def create_widgets(self):
        frm_header_bar = create_header(self,self.session_username.get())
        frm_header_bar.pack(fill=tk.X)

        
        #main frame
        main_frame= tk.Frame(master=self, 
                                width = 200, height=300, 
                                bg="yellow")
        for c in range(10):
            main_frame.columnconfigure(c, weight=1)
        for r in range(10):
            main_frame.rowconfigure(r, weight=1)
            
        #Payment screen    
        payment_screen = tk.Frame(master=main_frame, bg="blue", relief=tk.RAISED)
        payment_screen.grid(row=0,column=0,rowspan=7,columnspan=10,sticky="NSEW")
        df = gv.member_view_unpaidfines(self.session_username.get())
        self.fill_payment(df, payment_screen)

        
        
        #Create Buttons
        pay_button = tk.Button(master=main_frame, text="Pay Fines",width=8,height=3,command = lambda : self.payment_function(main_frame))
        pay_button.grid(row=8,column=2,columnspan = 1)
        cancel_button = tk.Button(master=main_frame, text="Cancel",width=8,height=3,command = lambda :self.controller.show_frame(self.controller.PAGES[1]))
        cancel_button.grid(row=8,column=7, columnspan = 1)
            
        
            

        

        main_frame.pack(fill=tk.BOTH, padx=20, pady=(0,10),expand=True)
        
    
    def fill_payment(self, df, frame):
        
        #Create title
        title_frame = tk.Frame(master=frame, bg = "blue")
        for c in range(2):
            title_frame.columnconfigure(c, weight=1)
            
        book_name = tk.Label(master=title_frame,text="Fine Date", width = 10, font=('', 15))
        book_name.grid(row=1,column=0)
            
        due_date = tk.Label(master=title_frame,text="Fine Amount", width = 10, font=('', 15))
        due_date.grid(row=1,column=1)
        
        title_frame.pack(fill = tk.X , side = tk.TOP)
        
        #Making individual frames
        #Assume: index < 4 
        for index, row in df.iterrows():
            #Create frame
            new_frame = tk.Frame(master=frame, bg = "blue")
            #Create grid
            for c in range(2):
                new_frame.columnconfigure(c, weight=1)
            #Book data
            book_name = tk.Label(master=new_frame,text=row[0], width = 10, font=('', 15))
            book_name.grid(row=1,column=0)
            
            due_date = tk.Label(master=new_frame,text="$" + str(row[1]) + ".0", width = 10, font=('', 15))
            due_date.grid(row=1,column=1)
            
            new_frame.pack(fill = tk.X , side = tk.TOP)
            
        total_label = tk.Label(master=frame, text = "Total Fine: $" + str(self.user_fines.get()),
                                                                    foreground="red", font=('', 20))
        total_label.pack(side = tk.BOTTOM)
        
    def payment_function(self, frame):
        if fm.no_unpaid_fine(self.session_username.get()):
            text = tk.Label(master = frame, text = "You do not have any outstanding fines.", foreground="red")
            text.grid(row= 10, column = 4, columnspan = 2)
        elif not fm.returned_overduebks(self.session_username.get()):
            text = tk.Label(master = frame, text = "Please return all overdue books before making payment.", foreground="red")
            text.grid(row= 10, column = 3, columnspan = 4)
        else:
            fm.make_payment(self.session_username.get())
            #Transition to payment_statement.py

        
        
              
        
        
        


        
                


root = tk.Tk()
root.geometry('600x600')
root.minsize(600,600)
container = tk.Frame(root)
container.pack(side = "top", fill = "both", expand = True) 
container.grid_rowconfigure(0, weight = 1)
container.grid_columnconfigure(0, weight = 1)
frame = NewPaymentWindow(container,root)
frame.grid(row = 0, column = 0, sticky ="nsew")
frame.tkraise()
root.mainloop()  