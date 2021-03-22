import tkinter as tk
from tkinter import ttk #we will use this later on...

from datetime import datetime

import Bk_Manager as bk
import GetViews as gv
import bookborrow as bb
import FP_Manager as FP

#from page_payment import PaymentPage

class HomePage(tk.Frame):    
    def __init__(self, parent, controller, session_user_data):
        super().__init__(parent)
        self.parent,self.controller = parent, controller 
        
        ## Unpack User Session Variables ##
        print(session_user_data)
        self.user_data = session_user_data
        self.user_name =  session_user_data["userId"]
        self.user_data["borrowed"] = []
        self.user_data["reserved"] = []
        
        ## For user fines ##
        self.user_fines = tk.DoubleVar()
        self.get_fines()
        
        ## Initialize ##
        self.create_widgets()
    
    def get_fines(self):
        #Get total fines
        total_fines = gv.member_view_totalfineamount(self.user_name)
        self.user_fines.set(total_fines)
        self.user_data["unpaid_fines"] = True if total_fines > 0 else False
        
    def create_widgets(self):
        """
        Use the following widget abbreviations
        Label 	lbl 	lbl_name
        Button 	btn 	btn_submit
        Entry 	ent 	ent_age
        Text 	txt 	txt_notes
        Frame 	frm 	frm_address
        """
        #### Page Content ####
        frm_content = tk.Frame(master=self)
        frm_content.columnconfigure(0,weight=1)
        frm_content.rowconfigure(0,weight=1) 
        frm_content.rowconfigure(1,weight=7) 
        frm_content.rowconfigure(2,weight=6)
        frm_content.pack(fill=tk.BOTH,pady=(5,20),expand=True)
        
        # Some general styling vars
        HOME_CONTENT_PADX = 20
        

        #### Borrowed Books display ####
        frm_middle= tk.Frame(master=frm_content, borderwidth=1, relief=tk.GROOVE,
                               bg = "white")
        frm_middle.grid(row=1,column=0,padx=HOME_CONTENT_PADX,sticky="nsew")
        
        ## Populate the display ##
        df = gv.member_view_bksborrowed(self.user_name)
        self.fill_borrow(df, frm_middle)
        
        #### Reserved Books and Pay Fines Display ####
        # Frame is a 1x2 grid 
        frm_bottom = tk.Frame(master=frm_content)
        frm_bottom.grid(row=2,column=0,padx=HOME_CONTENT_PADX,pady=(10,0),sticky="nsew") 
        frm_bottom.rowconfigure(0,weight=1)
        
        ### Reserved Books Display: 75% size
        frm_bottom.columnconfigure(0, weight=3)
        frm_reserved = tk.Frame(master=frm_bottom,bg="white",
                                relief=tk.GROOVE,borderwidth=1)
        frm_reserved.grid(row=0, column=0, padx=(0,10),sticky="nsew")
        ## Populate the display ##
        reserve_df = gv.member_view_bksreserved(self.user_name)
        self.fill_reserve(reserve_df,frm_reserved, frm_middle)

        ### Fines Display: 25% size
        frm_bottom.columnconfigure(1, weight=1)
        frm_fines = tk.Frame(master=frm_bottom,bg="white",
                             relief=tk.GROOVE,borderwidth=1)
        frm_fines.grid(row=0, column=1, sticky="nsew")
        
        ## Sub-Container
        frm_fines.grid_rowconfigure(0, weight=1)
        frm_fines.grid_columnconfigure(0, weight=1)
        frm_fines_c = tk.Frame(master=frm_fines,bg="white")
        frm_fines_c.grid(row=0, column=0, sticky="")

        #Info text
        lbl_fine_txt = tk.Label(master=frm_fines_c, bg="white",
                                text="Fines payable", font=('', 12,'bold'))
        lbl_fine_txt.pack(fill=tk.X)

        lbl_fine_amt = tk.Label(master=frm_fines_c,text= "$" + str(self.user_fines.get()), 
                                foreground="red", font=('', 12),bg="white")
        lbl_fine_amt.pack(fill=tk.X)
        #Pay fines button
        btn_pay_fine = tk.Button(master=frm_fines_c,text="Pay",pady=5,
                                 command=self.controller.on_pay_btn_press)
        btn_pay_fine.pack(fill=tk.X,pady=(0,15))
        
    #Fill up Borrowed Book Frame
    def fill_borrow(self, df, frame):
        ## Container Frame ##
        frm_borrowed = tk.Frame(master=frame, bg = "white")
        frm_borrowed.pack(fill = tk.X , side = tk.TOP)
        # Configure Grid
        for c in range(3):
            frm_borrowed.columnconfigure(c,weight=1)
        for r in range(5):
            frm_borrowed.rowconfigure(r,weight=1)

        ## Headers ##
        head_font = ('', 15,'bold')
        book_name = tk.Label(master=frm_borrowed,text="Borrowed Books", 
                             width = 25, font=head_font,bg="white")
        book_name.grid(row=0,column=0, pady=(0,5))
        due_date = tk.Label(master=frm_borrowed,text="Due Date", 
                            width = 10, font=head_font,bg="white")
        due_date.grid(row=0,column=1, pady=(0,5))
        action = tk.Label(master=frm_borrowed,text="Extend", 
                          width = 10, font=head_font, bg="white")
        action.grid(row=0,column=2, pady=(0,5))
        
        ## Borrowed Book records, max 4 ##
        for index, row in df.iterrows():
            #Add to session data
            self.user_data["borrowed"].append(row[0])
            print(self.user_data["borrowed"])
            
            #Book data
            book_name = tk.Label(master=frm_borrowed,text=row[1],height = 2, 
                                 width = 25, font=('', 15), bg="white",
                                 wraplength=250)
            book_name.grid(row=index+1,column=0, pady=(0,5))
            
            due_date = tk.Label(master=frm_borrowed,text=row[2],
                                width = 10, font=('', 15), bg="white")
            due_date.grid(row=index+1,column=1,pady=(0,5))
            
            ## Action (Extend) button
            #check if book is late
            date = datetime.strptime(str(row[2]), "%Y-%m-%d")
            current = datetime.now()
            if date.date() <= current.date(): #Late
                action = tk.Label(master=frm_borrowed,text="Late", foreground = "red", 
                                  width = 10, font=('', 15), bg="white")
            elif bb.is_reserved(row[0]):
                action = tk.Label(master=frm_borrowed,text="No Extension", 
                                  foreground = "red", width = 10, font=('', 15), bg="white")
            else:
                action = tk.Button(master=frm_borrowed, text="Extend", 
                                          width = 10, font=('', 13))
                action['command'] = lambda button = action, due_date = due_date, row = row, index = index+1,: self.extend(due_date, frm_borrowed, row[0], index, button)
            
            action.grid(row=index+1,column=2, pady=(0,5))
        
        ## Message Box ##
        self.borrow_message = tk.Label(master=frame,text="", bg="white",
                                      foreground = "red", font=('', 15))
        self.borrow_message.pack(side=tk.BOTTOM)
                
    #Fill up Reserved Book Frame               
    def fill_reserve(self, df, frame, add_frame):
        
        #Create title
        title_frame = tk.Frame(master=frame, bg = "yellow")
        for c in range(4):
            title_frame.columnconfigure(c, weight=1)
            
        book_name = tk.Label(master=title_frame,text="Reserved Books", width = 25)
        book_name.grid(row=1,column=0)
            
        due_date = tk.Label(master=title_frame,text="Expexted Date", width = 10)
        due_date.grid(row=1,column=1)
        
        status = tk.Label(master=title_frame,text="Status", width = 6)
        status.grid(row=1,column=2)        
        
        cancel = tk.Label(master=title_frame,text="Cancel", width = 6)
        cancel.grid(row=1,column=3)
        
        title_frame.pack(fill = tk.X , side = tk.TOP)
        
        #Making individual frames
        #Assume: index < 4 
        for index, row in df.iterrows():
            #Create frame
            new_frame = tk.Frame(master=frame, bg = "yellow")
            #Create grid
            for c in range(4):
                new_frame.columnconfigure(c, weight=1)
            #Book data
            book_name = tk.Label(master=new_frame,text=row[1], width = 25)
            book_name.grid(row=1,column=0)
            
            expected_date = tk.Label(master=new_frame,text=row[2], width = 10)
            expected_date.grid(row=1,column=1)
            
            #Add to session data
            self.user_data["reserved"].append(row[0])
            
            if not bk.check_status(row[0]):
                status = tk.Label(master=new_frame,text="Reserved", width = 6, foreground = "red")
                status.grid(row=1,column=2)
                
            elif not FP.no_unpaid_fine(self.user_name):
                status = tk.Label(master=new_frame,text="Fined", width = 6, foreground = "red")
                status.grid(row=1,column=2)
            
            elif bb.is_max_book(self.user_name):
                status = tk.Label(master=new_frame,text="Limit", width = 6, foreground = "red")
                status.grid(row=1,column=2)    
                            
            else:
                status = tk.Button(master=new_frame,text="Borrow", width = 6, foreground = "green", command = lambda frame = new_frame, row = row, add_frame = add_frame: self.borrow(frame, add_frame, row, self.user_name))
                status.grid(row=1,column=2)                
                
            
            cancel_button = tk.Button(master=new_frame, text="Cancel", command = lambda row = row, new_frame = new_frame : self.cancel(new_frame, self.user_name, row[0]))
            cancel_button.grid(row=1,column=3)
            
            new_frame.pack(fill = tk.X , side = tk.TOP)
            
    def cancel(self, frame, user_id, book_id) :
        bk.cancel_reservation(book_id, user_id)
        frame.pack_forget()
        
    def extend(self, due_date_label,frame, book_id, index, button):
        message = bk.extend_borrowing(book_id, self.user_name)
        self.borrow_message.config(text=message)
        button.destroy()
        extension_label = tk.Label(master=frame,text="Extended", bg="white",
                                   foreground = "green", font=('', 15), width = 10)
        extension_label.grid(row=index,column=2,pady=(0,5))
        due_date_label.configure(text = gv.get_new_due_date(book_id))
        
    def borrow(self, frame, add_frame, row, user_id):
        #Check number of Books
        if bb.is_max_book(self.user_name):
            status = tk.Label(master=add_frame,text="Maximum Books Borrowed", width = 6, foreground = "red")
            status.pack(side = tk.BOTTOM, fill = tk.X)
        
        else:
            bb.borrow_book(row[0], user_id)
            bk.cancel_reservation(row[0], user_id)
            frame.pack_forget()
            #Create frame
            new_frame = tk.Frame(master=add_frame, bg = "red")
            #Create grid
            for c in range(3):
                new_frame.columnconfigure(c, weight=1)
            #Book data
            book_name = tk.Label(master=new_frame,text=row[1], width = 25, font=('', 15), height = 2)
            book_name.grid(row=1,column=0)
            
            due_date = tk.Label(master=new_frame,text=gv.get_new_due_date(row[0]), width = 10, font=('', 15))
            due_date.grid(row=1,column=1)
            
            if bb.is_reserved(row[0]):
                cancel = tk.Label(master=new_frame,text="No Extension", foreground = "red", width = 10, font=('', 15))
                cancel.grid(row=1,column=2)
            else:
                extend_button = tk.Button(master=new_frame, text="Extend", width = 10, font=('', 15))
                extend_button['command'] = lambda button = extend_button, due_date = due_date, row = row, index = index+1,: self.extend(due_date, frm_borrowed, row[0], index, button)
                extend_button.grid(row=1,column=2)
            
            new_frame.pack(fill = tk.X , side = tk.TOP)     

                   
## DEBUG USE ONLY ###
if __name__ == '__main__':
    root = tk.Tk()
    container = tk.Frame(root)
    container.pack(side = "top", fill = "both", expand = True) 
    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)
    
    test_user = {"userId": "willywonka69"}
    
    frame = HomePage(container,root,test_user)
    frame.grid(row = 0, column = 0, sticky ="nsew")
    frame.tkraise()
    root.mainloop()  