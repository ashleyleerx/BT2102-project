import tkinter as tk
from tkinter import ttk #we will use this later on...




import Bk_Manager as bk
import GetViews as gv
import bookborrow as bb
import FP_Manager as FP

from header import create_header

class HomePage(tk.Frame):    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent,self.controller = parent, controller 
        controller.title("Homepage")
        #Session Variables
        self.session_username = tk.StringVar()
        self.user_fines = tk.DoubleVar()
        #Get total fines
        self.user_fines.set(gv.member_view_totalfineamount(self.session_username.get()))
        self.search_text = tk.StringVar(value="Search Catalogue") 
        
        ### DEVELOPMENT ONLY ###
        self.session_username.set("danielpo") 
        self.user_fines.set(gv.member_view_totalfineamount(self.session_username.get()))        
        self.create_widgets()
        print(self.user_fines.get())

      
    def create_widgets(self):
        """
        Use the following widget abbreviations
        Label 	lbl 	lbl_name
        Button 	btn 	btn_submit
        Entry 	ent 	ent_age
        Text 	txt 	txt_notes
        Frame 	frm 	frm_address
        """
        
        #### Header Bar ####
        frm_header_bar = create_header(self,self.session_username.get())
        frm_header_bar.pack(fill=tk.X)
        
        #### Page Content ####
        frm_content = tk.Frame(master=self)
        frm_content.columnconfigure(0,weight=1)
        frm_content.rowconfigure(0,weight=1) 
        frm_content.rowconfigure(1,weight=10) 
        frm_content.rowconfigure(2,weight=3)
        frm_content.pack(fill=tk.BOTH,pady=10,expand=True)
        
        # Some general styling vars
        HOME_CONTENT_PADX = 20
        

        #### Borrowed Books display ####
        frm_borrowed= tk.Frame(master=frm_content, borderwidth=1,bg = "red")
        
        ## Add to layout
        frm_borrowed.grid(row=1,column=0,padx=HOME_CONTENT_PADX,sticky="nsew")
        
        ## Member books borrowed
        df = gv.member_view_bksborrowed(self.session_username.get())
        self.fill_borrow(df, frm_borrowed)
        
        
        
        #### Reserved Books and Pay Fines Display ####
        frm_bottom = tk.Frame(master=frm_content,bg="blue")
        #bottom frame is 1x2 grid - consists of following elements:
        frm_bottom.rowconfigure(0,weight=1)
        ### Reserved Books Display: 75% size
        frm_bottom.columnconfigure(0, weight=3)
        frm_reserved = tk.Frame(master=frm_bottom,bg="yellow",
                                relief=tk.RAISED,borderwidth=1)
        frm_reserved.grid(row=0, column=0, padx=10, pady=10,sticky="nsew")
        
        ## Member books reserved
        #print("user: " + self.session_username.get())
        reserve_df = gv.member_view_bksreserved(self.session_username.get())
        self.fill_reserve(reserve_df,frm_reserved, frm_borrowed)

    
        ### Fines Display: 25% size
        frm_bottom.columnconfigure(1, weight=1)
        frm_fines = tk.Frame(master=frm_bottom,bg="green",
                             relief=tk.RAISED,borderwidth=1)
        frm_fines.grid(row=0, column=1, padx=10, pady=10,sticky="nsew")
        
        ## Sub-Container
        frm_fines.grid_rowconfigure(0, weight=1)
        frm_fines.grid_columnconfigure(0, weight=1)
        frm_fines_c = tk.Frame(master=frm_fines,bg="pink")
        
        #Info text
        lbl_fine_txt = tk.Label(master=frm_fines_c,text="Fines payable", font=('', 12))
        lbl_fine_txt.pack(fill=tk.X)

        lbl_fine_amt = tk.Label(master=frm_fines_c,text= "$" + str(self.user_fines.get()), 
                                foreground="red", font=('', 12))
        lbl_fine_amt.pack(fill=tk.X)
        #Pay fines button
        btn_pay_fine = tk.Button(master=frm_fines_c,text="Pay")
        btn_pay_fine.pack(fill=tk.X)
        #TO-DO fancy highlighting thing
        
        frm_fines_c.grid(row=0, column=0, sticky="",ipadx=10,ipady=10)
        
        ### Packing frame bottom ###
        ## Add to layout
        frm_bottom.grid(row=2,column=0,padx=HOME_CONTENT_PADX,pady=(10,0),sticky="nsew")
        
    #Fill up Borrowed Book Frame
    def fill_borrow(self, df, frame):
        #Create title
        title_frame = tk.Frame(master=frame, bg = "red")
        for c in range(3):
            title_frame.columnconfigure(c, weight=1)
            
        book_name = tk.Label(master=title_frame,text="Borrowed Books", width = 25, font=('', 15))
        book_name.grid(row=1,column=0)
            
        due_date = tk.Label(master=title_frame,text="Due Date", width = 10, font=('', 15), foreground = "red")
        due_date.grid(row=1,column=1)
        
        cancel = tk.Label(master=title_frame,text="Extend", width = 10, font=('', 15))
        cancel.grid(row=1,column=2)
        
        title_frame.pack(fill = tk.X , side = tk.TOP)
        
        #Making individual frames
        #Assume: index < 4 
        for index, row in df.iterrows():
            #Create frame
            new_frame = tk.Frame(master=frame, bg = "red")
            #Create grid
            for c in range(3):
                new_frame.columnconfigure(c, weight=1)
            #Book data
            book_name = tk.Label(master=new_frame,text=row[1], width = 25, font=('', 15), height = 2)
            book_name.grid(row=1,column=0)
            
            due_date = tk.Label(master=new_frame,text=row[2], width = 10, font=('', 15))
            due_date.grid(row=1,column=1)
            
            if bb.is_reserved(row[0]):
                cancel = tk.Label(master=new_frame,text="No Extension", foreground = "red", width = 10, font=('', 15))
                cancel.grid(row=1,column=2)
            else:
                extend_button = tk.Button(master=new_frame, text="Extend", width = 10, font=('', 15))
                extend_button['command'] = lambda button = extend_button, mini_frame = new_frame, due_date = due_date, row = row: self.extend(due_date, frame, self.session_username.get(), row[0], mini_frame, button)
                extend_button.grid(row=1,column=2)
            
            new_frame.pack(fill = tk.X , side = tk.TOP)
                
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
            
            if not bk.check_status(row[0]):
                status = tk.Label(master=new_frame,text="Reserved", width = 6, foreground = "red")
                status.grid(row=1,column=2)
                
            elif not FP.no_unpaid_fine(self.session_username.get()):
                status = tk.Label(master=new_frame,text="Fined", width = 6, foreground = "red")
                status.grid(row=1,column=2)
            
            elif bb.is_max_book(self.session_username.get()):
                status = tk.Label(master=new_frame,text="Limit", width = 6, foreground = "red")
                status.grid(row=1,column=2)    
                            
            else:
                status = tk.Button(master=new_frame,text="Borrow", width = 6, foreground = "green", command = lambda frame = new_frame, row = row, add_frame = add_frame: self.borrow(frame, add_frame, row, self.session_username.get()))
                status.grid(row=1,column=2)                
                
            
            cancel_button = tk.Button(master=new_frame, text="Cancel", command = lambda row = row, new_frame = new_frame : self.cancel(new_frame, self.session_username.get(), row[0]))
            cancel_button.grid(row=1,column=3)
            
            new_frame.pack(fill = tk.X , side = tk.TOP)
            
    def cancel(self, frame, user_id, book_id) :
        bk.cancel_reservation(book_id, user_id)
        frame.pack_forget()
        
    def extend(self, label, frame, user_id, book_id, mini_frame, button):
        message = bk.extend_borrowing(book_id, user_id)
        message_label = tk.Label(master=frame,text=message, foreground = "red", font=('', 15))
        button.destroy()
        extension_label = tk.Label(master=mini_frame,text="Extended", foreground = "green", font=('', 15), width = 10)
        extension_label.grid(row=1,column=2)
        label.configure(text = gv.get_new_due_date(book_id))
        message_label.pack(side = tk.BOTTOM)
        
    def borrow(self, frame, add_frame, row, user_id):

        
        #Check number of Books
        if bb.is_max_book(self.session_username.get()):
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
            
            if bb.is_max_book(row[0]):
                cancel = tk.Label(master=new_frame,text="No Extension", foreground = "red", width = 10, font=('', 15))
                cancel.grid(row=1,column=2)
            else:
                extend_button = tk.Button(master=new_frame, text="Extend", width = 10, font=('', 15))
                extend_button['command'] = lambda button = extend_button, mini_frame = new_frame, due_date = due_date, row = row: self.extend(due_date, frame, self.session_username.get(), row[0], mini_frame, button)
                extend_button.grid(row=1,column=2)
            
            new_frame.pack(fill = tk.X , side = tk.TOP)       
        
        

            

                
                
    
            
                             
                
            
 
        
## DEBUG USE ONLY ###
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x600')
    root.minsize(600,600)
    container = tk.Frame(root)
    container.pack(side = "top", fill = "both", expand = True) 
    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)
    frame = HomePage(container,root)
    frame.grid(row = 0, column = 0, sticky ="nsew")
    frame.tkraise()
    root.mainloop()  