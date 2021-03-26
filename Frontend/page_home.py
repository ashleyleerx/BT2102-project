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
        frm_content.pack(fill=tk.BOTH,pady=(5,20),expand=True)
        frm_content.columnconfigure(0,weight=1)
        frm_content.rowconfigure(0,weight=60) 
        frm_content.rowconfigure(1,weight=40)
        
        # Some general styling vars
        HOME_CONTENT_PADX = 20
        
        #### Borrowed Books display ####
        frm_middle= tk.Frame(master=frm_content, borderwidth=1, relief=tk.GROOVE,
                             height=360,width=200,
                             bg = "white")
        frm_middle.grid(row=0,column=0,padx=HOME_CONTENT_PADX,sticky="nsew")
        
        ## Populate the display ##
        df = gv.member_view_bksborrowed(self.user_name)
        self.fill_borrow(df, frm_middle)
        
        #### Reserved Books and Pay Fines Display ####
        # Frame is a 1x2 grid 
        frm_bottom = tk.Frame(master=frm_content,bg="white")
        frm_bottom.grid(row=1,column=0,padx=HOME_CONTENT_PADX,pady=(10,0),sticky="nsew") 
        frm_bottom.rowconfigure(0,weight=1)
        
        ### Reserved Books Display: 75% size
        frm_bottom.columnconfigure(0, weight=3)
        self.frm_reserved = tk.Frame(master=frm_bottom,bg="white",
                                relief=tk.GROOVE,borderwidth=1)
        self.frm_reserved.grid(row=0, column=0, padx=(0,10),sticky="nsew")
        self.frm_reserved.rowconfigure(0,weight=1)
        self.frm_reserved.columnconfigure(0,weight=1)
        
        ## Populate the display ##
        reserve_df = gv.member_view_bksreserved(self.user_name)
        self.fill_reserve(reserve_df, None)

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
        btn_pay_fine = tk.Button(master=frm_fines_c,text="Pay",pady=5)
                                 #command=self.controller.on_pay_btn_press)
        btn_pay_fine.pack(fill=tk.X,pady=(0,15))
        
    #Fill up Borrowed Book Frame
    def fill_borrow(self, df, frame):
        ## Container Frame ##
        frm_borrowed = tk.Frame(master=frame, bg = "white")
        frm_borrowed.pack(side=tk.TOP, fill=tk.BOTH)
        self.borrowed_ref = frm_borrowed
        # Configure Grid
        for c in range(3):
            frm_borrowed.columnconfigure(c,weight=1)
            
        #Fill data
        table_data = [["","Borrowed Books", "Due Date", "Extend"],
                      ["","","",""],
                      ["","","",""],
                      ["","","",""],
                      ["","","",""]]
        ## Borrowed Book records, max 4 ## 
        for index, row in df.iterrows():
            self.user_data["borrowed"].append(row[0])
            table_data[index+1] = [row[0],row[1],row[2],""]
        
        ## Fill frame 
        for index,row in enumerate(table_data):
            self.add_borrowed_row(index,row,frm_borrowed)
                
        ## Message Box ##
        # self.borrow_message = tk.Label(master=frame,text="", bg="green",
        #                               foreground = "red", font=('', 15))
        # self.borrow_message.pack()

    def add_borrowed_row(self,index,row_vals,frame):
        row_font =('', 15)
        book_name = tk.Label(master=frame,text=row_vals[1], 
                                width = 25, bg="white",font=row_font)
        due_date = tk.Label(master=frame,text=row_vals[2], 
                            width = 10, bg="white",font=row_font)
        action = tk.Label(master=frame,text=row_vals[3], 
                            width = 10, bg="white",font=row_font)
    
        if(index == 0): #Header
            head_font = ('', 15,'bold')
            book_name.config(font=head_font)
            due_date.config(font=head_font)
            action.config(font=head_font)
        else:
            book_name.config(height=2, wraplength=250)
            if (row_vals[2] != ""): 
                date = datetime.strptime(str(row_vals[2]), "%Y-%m-%d")
                current = datetime.now()
            
                if date.date() <= current.date(): #Late
                    action.config(text="Late", fg = "red")
                elif bb.is_reserved(row_vals[0]):
                    action.config(text="No Extension", fg = "red")
                else:
                    action = tk.Button(master=frame, text="Extend", width = 10, font=('', 13))
                    action['command'] = lambda button = action, due_date = due_date, index = index,: self.extend(due_date, frame, row_vals[0], index, button)
        
        book_name.grid(row=index,column=0, pady=(0,10))
        due_date.grid(row=index,column=1, pady=(0,10))
        action.grid(row=index,column=2, pady=(0,10))
                        
    #Fill up Reserved Book Frame               
    def fill_reserve(self, df, exisiting):
        if exisiting:
            self.user_data["reserved"] = []
            exisiting.destroy()
        
        reserved_container = tk.Frame(master=self.frm_reserved, bg="white")
        reserved_container.grid(row=0,column=0,sticky="nsew")
        #Create title
        title_frame = tk.Frame(master=reserved_container, bg = "white")
        title_frame.pack(fill = tk.X , side = tk.TOP)
        for c in range(4):
            title_frame.columnconfigure(c, weight=1)
        
        head_font = ('', 10,'bold')
        book_name = tk.Label(master=title_frame,text="Reserved Books", bg="white",
                             width = 23, font=head_font)
        book_name.grid(row=0,column=0)
        due_date = tk.Label(master=title_frame,text="Expected Date", bg="white",
                            width = 11, font=head_font)
        due_date.grid(row=0,column=1)
        status = tk.Label(master=title_frame,text="Status", bg="white",
                          width = 6, font=head_font)
        status.grid(row=0,column=2)        
        cancel = tk.Label(master=title_frame,text="Cancel", bg="white",
                          width = 6, font=head_font)
        cancel.grid(row=0,column=3)
        
        #Making individual frames
        #Assume: index < 4 
        for index, row in df.iterrows():
            row_font = ('',10)
            #Create frame
            new_frame = tk.Frame(master=reserved_container, bg = "white")
            #Create grid
            for c in range(4):
                new_frame.columnconfigure(c, weight=1)
            #Book data
            book_name = tk.Label(master=new_frame,text=row[1], width = 23, 
                                 font = row_font, bg = 'white',
                                 wraplength=300)
            book_name.grid(row=0,column=0)
            
            expected_date = tk.Label(master=new_frame,text=row[2], width = 11, 
                                     font=row_font, bg= "white")
            expected_date.grid(row=0,column=1)
            
            #Add to session data
            self.user_data["reserved"].append(row[0])
            
            status = tk.Label(master=new_frame,text="", width = 6, foreground = "red",
                              font=row_font, bg= "white")
            
            if not bk.check_status(row[0]):
                status.config(text="Reserved")
            elif self.user_data["unpaid_fines"]:
                status.config(text="Fined")
            elif bb.is_max_book(self.user_name):
                status.config(text="Limit")          
            else:
                status = tk.Button(master=new_frame,text="Borrow", font=row_font,
                                   width = 6, foreground = "green", bg="white",
                                   command = lambda frame=reserved_container, row = row: self.borrow(frame, row, self.user_name))           
            status.grid(row=0,column=2)
            
            cancel_button = tk.Button(master=new_frame, text="Cancel", padx=5,
                                      command = lambda row = row, new_frame = new_frame : self.cancel(new_frame, self.user_name, row[0]))
            cancel_button.grid(row=0,column=3)
            
            new_frame.pack(fill = tk.X , side = tk.TOP, pady=(5,0))
            
    def cancel(self, frame, user_id, book_id) :
        bk.cancel_reservation(book_id, user_id)
        frame.pack_forget()
        
    def extend(self, due_date_label,frame, book_id, index, button):
        message = bk.extend_borrowing(book_id, self.user_name)
        #self.borrow_message.config(text=message)
        button.destroy()
        extension_label = tk.Label(master=frame,text="Extended", bg="white",
                                   foreground = "green", font=('', 15), width = 10)
        extension_label.grid(row=index,column=2,pady=(0,10))
        due_date_label.configure(text = gv.get_new_due_date(book_id))
        
    def borrow(self,frame,row, user_id):
        #Check number of Books
        if bb.is_max_book(self.user_name):
            print("Max Books")
            #status = tk.Label(master=add_frame,text="Maximum Books Borrowed", width = 6, foreground = "red")
            #status.pack(side = tk.BOTTOM, fill = tk.X)
        else:
            bb.borrow_book(row[0], user_id)
            bk.cancel_reservation(row[0], user_id)
            # Add to borrowed list
            new_i = len(self.user_data["borrowed"]) + 1
            self.add_borrowed_row(new_i,[row[0],row[1],gv.get_new_due_date(row[0]),""],self.borrowed_ref)
            self.user_data["borrowed"].append(row[0])
            # Refresh reserved list
            reserve_df = gv.member_view_bksreserved(self.user_name)
            self.fill_reserve(reserve_df,frame)
            
            
            
    
## DEBUG USE ONLY ###
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("600x600")
    root.minsize(600,600)
    
    container = tk.Frame(root)
    container.pack(side = "top", fill = "both", expand = True) 
    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)
    
    test_user = {"userId": "henrychia07"}
    
    frame = HomePage(container,root,test_user)
    frame.grid(row = 0, column = 0, sticky ="nsew")
    frame.tkraise()
    root.mainloop()  