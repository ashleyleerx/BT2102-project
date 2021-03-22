from datetime import datetime, timedelta
import tkinter as tk
from tkinter import OptionMenu, ttk
from tkinter.constants import ACTIVE, DISABLED  # we will use this later on...
from tkinter import messagebox
import pandas as pd

import BkSearch as bksearch
import bookborrow as bkborrow

options = {"Title": [], "ISBN": [], 
           "Page Count": ["Lesser", "Equal", "Greater"],
           "Published Year": ["Before", "Equal", "After"], 
           "Categories": [], "Authors": []}

class SearchDisplay(tk.Frame):
    def __init__(self, parent, controller, session_user_data):
        super().__init__(parent)
        self.parent, self.controller = parent, controller
        ## Unpack User Session Variables ##
        print(session_user_data)
        self.user_data = session_user_data
        self.user_name =  session_user_data["userId"]
        self.user_unpaid_fines = session_user_data["unpaid_fines"]
        self.user_borrowed = session_user_data["borrowed"]
        self.user_reserved = session_user_data["reserved"]
    
        ## Page Variables ##
        # Search Bar #
        self.search_text = tk.StringVar()
        self.adv_dropdown = tk.StringVar()
        self.adv_dropdown.set("")
        self.sub_adv_dropdown = tk.StringVar()
        self.sub_adv_dropdown.set("")
        # Search Results Treeview Display #
        self.treedata = tk.StringVar()
        
        # Book Details Display #
        self.bk_title = tk.StringVar()
        self.bk_author = tk.StringVar()
        self.bk_desc = tk.StringVar()
        self.bk_status = tk.StringVar()
        
        self.bk_selected_id = -1 #Currently selected BookId
        self.bk_selected_title = ""
        self.bk_selected_due = ""

        self.create_widgets()

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
        frm_content.columnconfigure(0, weight=1)
        frm_content.rowconfigure(0, weight=1)
        frm_content.rowconfigure(1, weight=10)
        frm_content.rowconfigure(2, weight=2)
        frm_content.pack(fill=tk.BOTH, pady=(5,20), expand=True)

        # Some general styling vars
        HOME_CONTENT_PADX = 20

        ### Search ###
        frm_search = tk.Frame(master=frm_content, borderwidth=1)
        frm_search.grid(row=0, column=0, padx=HOME_CONTENT_PADX,
                        pady=(0, 10), sticky="nsew")

        ## Top row: Header and Error Display ##
        frm_search_top = tk.Frame(master=frm_search)
        frm_search_top.pack(fill=tk.X,pady=(5,0))
        # Label #
        lbl_search = tk.Label(master=frm_search_top,text="Search Catalog")
        lbl_search.pack(side=tk.LEFT,anchor="w",padx=(0,10))
        # Error Display
        self.lbl_msg_display = tk.Label(frm_search_top, text="", font=("", 10))
        self.lbl_msg_display.pack(side=tk.LEFT,anchor="w")

        ## Top row : Entry + Button ##
        frm_search_mid = tk.Frame(master=frm_search)
        frm_search_mid.pack(fill=tk.BOTH, expand=True)

        # Search Entry #
        search_bar = tk.Entry(master=frm_search_mid,
                              textvariable=self.search_text)
        search_bar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Search Button #
        btn_search = tk.Button(master=frm_search_mid, text="Search", height=1, padx=10,
                               bg="lightblue",activebackground="lightblue",
                               command=self.on_search_req_btn_press)
        btn_search.pack(side=tk.RIGHT, fill=tk.Y,padx=(5,0))

        
        # Bottom row - Advanced search
        frm_search_btm = tk.Frame(master=frm_search)
        frm_search_btm.pack(fill=tk.X, expand=True, pady=(5,0))

        # Drop Down: Advanced Search #
        self.drop = ttk.Combobox(frm_search_btm,state="readonly",width=15)
        self.drop['values'] = list(options.keys())
        self.drop.current(0)
        self.drop.pack(side=tk.LEFT, fill=tk.Y)
        self.drop.bind('<<ComboboxSelected>>', self.getUpdateData)

        # Drop Down: Sub Advanced Search #
        self.sub_drop = ttk.Combobox(frm_search_btm, state="readonly",width=10)
        
        #### Search Result Display Treeview ####
        frm_results = tk.Frame(master=frm_content, borderwidth=1)
        # browse - only 1 item can be selected
        tv = ttk.Treeview(frm_results, selectmode="browse")
        tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ## Configure Treeview ##
        HEADINGS = ('Id', 'Title', 'Status', 'Reserved')
        tv['columns'] = HEADINGS
        tv["show"] = "headings"  # supresses icon(#0) column
        # tv.heading("#0", text='Sources', anchor='w')
        # tv.column("#0", anchor="w")

        # Set headings (column names)
        for h in HEADINGS:
            tv.heading(h, text=h)
        # Set column sizing
        tv.column(HEADINGS[0], anchor='center', width=40,
                  minwidth=40, stretch=True)
        tv.column(HEADINGS[1], anchor='w',
                  width=300, minwidth=200, stretch=True)
        tv.column(HEADINGS[2], anchor='center',
                  width=100, minwidth=80, stretch=True)
        tv.column(HEADINGS[3], anchor='center', width=100, stretch=True)

        # Bind event handlers
        # single click, without "index out of range" error
        tv.bind("<<TreeviewSelect>>", self.on_tree_select)

        ## Scrollbar for Treeview ##
        tvScroll = ttk.Scrollbar(frm_results, 
                                 orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=tvScroll.set)
        tvScroll.pack(side="right", fill='y')

        # Assign treeview
        self.treeview1 = tv

        # Add to layout
        frm_results.grid(row=1, column=0, padx=HOME_CONTENT_PADX, sticky="nsew")


        #### Master container for Book Display ####
        frm_bottom = tk.Frame(master=frm_content, height=150, 
                              bg="white",borderwidth=1,relief=tk.GROOVE)
        frm_bottom.grid(row=2, column=0, padx=HOME_CONTENT_PADX,
                        pady=(10, 0), sticky="nsew")
        frm_bottom.rowconfigure(0,weight=1)
        frm_bottom.columnconfigure(0,weight=1)

        #### Book Display ####
        frm_bkdispl = tk.Frame(master=frm_bottom,bg="white")
        frm_bkdispl.grid(row=0,column=0,padx=10,sticky="nsew")
        frm_bkdispl.grid_remove()
        self.frm_bkdip = frm_bkdispl
        
        ### Picture Display ###
        lbl_picture = tk.Canvas(frm_bkdispl, width = 120, height = 120,bg="pink")
        lbl_picture.pack(side=tk.LEFT,padx=(0,5))

        #### Book Details ###
        frm_bkdetails = tk.Frame(master=frm_bkdispl,bg="white",height=100,width=200)
        frm_bkdetails.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=(0,15),pady=10)
        # Title #
        lbl_bk_d_title = tk.Label(master=frm_bkdetails, textvariable=self.bk_title,
                                  font=('',10,'bold'),bg="white")
        lbl_bk_d_title.pack(anchor="w")
        # Author #
        lbl_bk_d_author = tk.Label(master=frm_bkdetails, textvariable=self.bk_author,
                                  font=('',10,'italic'),bg="white")
        lbl_bk_d_author.pack(anchor="w")
        # Desc #
        lbl_bk_d_desc = tk.Label(master=frm_bkdetails, textvariable=self.bk_desc,        
                                 justify="left",bg="white",anchor="nw",
                                 height=5,width=50,wraplength=300,
                                 font=('',8))
        lbl_bk_d_desc.pack(anchor="nw",expand=True,fill=tk.Y)

        ### Buttons ###
        frm_bk_btns = tk.Frame(master=frm_bkdispl, bg="white")
        frm_bk_btns.pack(side=tk.LEFT,anchor="n",pady=20,expand=False)
        
        frm_bk_btns.rowconfigure(0,weight=1)
        frm_bk_btns.rowconfigure(1,weight=1)
        frm_bk_btns.columnconfigure(0,weight=1)
        
        # Button Associated Message display #
        self.lbl_action_display = tk.Label(master=frm_bk_btns,text="",
                                           width=12,                                
                                           font=('',10,'italic'),bg="white")
        self.lbl_action_display.grid(row=0,column=0,pady=(0,5))
        
        # Borrow Button #
        self.btn_borrow = tk.Button(master=frm_bk_btns, text="Borrow", 
                                    height=2, padx=20, fg="White", bg="DarkGreen",
                                    state=tk.DISABLED, 
                                    command=self.on_borrow_btn_press)
        self.btn_borrow.grid(row=1, column=0)
        
        # # Extend Button #
        # self.btn_extend = tk.Button(master=frm_bk_btns, text="Extend", 
        #                             height=2, padx=20, fg="White", bg="LightBlue",
        #                             state=tk.DISABLED, 
        #                             command=self.on_extend_btn_press)
        # self.btn_extend.grid(row=1, column=0)
        # self.btn_extend.grid_remove()
                     
        # Reserve Button #
        self.btn_reserve = tk.Button(master=frm_bk_btns, text="Reserve", 
                                     height=2, padx=20, fg="White", bg="DarkGoldenRod",
                                     state=tk.DISABLED,
                                     command=self.on_reserve_btn_press)
        self.btn_reserve.grid(row=1, column=0)
        self.btn_reserve.grid_remove()
        
        # Cancel Button #
        # self.btn_cancel = tk.Button(master=frm_bk_btns, text="Cancel", 
        #                              height=2, padx=20, fg="White", bg="LightCoral",
        #                              state=tk.DISABLED,
        #                              command=self.on_cancel_btn_press)
        # self.btn_cancel.grid(row=1, column=0)
        # self.btn_cancel.grid_remove()
        
        
    ### UI EVENT HANDLERS ###
    def getUpdateData(self, event):
        sub_vals = options[self.drop.get()]
        sub_disp = self.sub_drop.winfo_ismapped()
        
        if sub_vals == []: #no sub values 
            if sub_disp:
                self.sub_drop.pack_forget()
            return 
        if (not sub_disp):
            self.sub_drop.pack(side=tk.LEFT, fill=tk.Y,padx=(10,0))
    
        self.sub_drop['values'] = sub_vals

    def on_search_req_btn_press(self):
        if (not self.check_search_input()):
            return
        # Inputs valid:
        self.load_table1()

    def load_table1(self):
        search_df = self.search() #pandas df
        #Clear Treeview
        self.treeview1.delete(*self.treeview1.get_children())
        # Handle results
        if search_df.empty:
            self.lbl_msg_display.config(text="No results found", fg="red")
            if self.frm_bkdip.winfo_ismapped():
                self.frm_bkdip.grid_remove()
        else:
            self.search_results = search_df
            for index, row in search_df.iterrows():
                self.treeview1.insert('', 'end', values=(
                    index, row[0], row[1], row[2]))

    def on_tree_select(self, event):            
        item = self.treeview1.selection()[0]
        vals = self.treeview1.item(item, 'values')
        oVals = self.search_results.loc[int(vals[0]),:]
        
        #Show book details frame (if hidden)
        if not self.frm_bkdip.winfo_ismapped():
            self.frm_bkdip.grid()
        #Update the book details frame
        self.bk_title.set(vals[1])
        self.bk_author.set(oVals[4])
        self.bk_desc.set(oVals[5])
        #Update selection cursor
        self.bk_selected_id = int(vals[0])
        self.bk_selected_title = vals[1]
        if not oVals[3] == "NIL":
            self.bk_selected_due = oVals[3].strftime("%d/%m/%Y")
        print(self.bk_selected_due)
        #Update Buttons
        self.switch_button_states((vals[2],vals[3]))
        
    def switch_button_states(self,status):
        if self.user_unpaid_fines:
            return 
        
        #By default, extend and cancel buttons are hidden
        if not self.btn_borrow.winfo_ismapped():
            self.btn_borrow.grid()
        if self.btn_reserve.winfo_ismapped():
            self.btn_reserve.grid_remove()
        self.lbl_action_display.grid_configure(pady=(0,5))
            
        #Status[0]: Available, On Loan 
        #Status[1]: Reserved, Not Reserved 
        if status[0] == "Available":
            #Can Borrow 
            s = tk.NORMAL if len(self.user_borrowed) < 4 else tk.DISABLED
            self.btn_borrow.config(state=s)
            self.lbl_action_display.config(text="Available\nfor borrowing")
        else:
            #Cannot Borrow 
            self.btn_borrow.config(tk.DISABLED)
            self.btn_borrow.grid_remove()
            #Check whether the book is borrowed by the current user
            print(self.bk_selected_id,"|",self.bk_selected_title)
            if self.bk_selected_id in self.user_borrowed:
                # #Borrowed by user -> can extend
                # self.btn_extend.config(state=tk.NORMAL)
                # self.btn_extend.grid()
                msg = "You have\nborrowed\nthis item.\nDue Date:\n" + self.bk_selected_due
                self.lbl_action_display.config(text= msg)
            else:
                #Not borrowed by user
                #Check whether has been reserved
                if status[1] == "Not Reserved":
                    #Can Reserve 
                    self.btn_reserve.config(state=tk.NORMAL)
                    self.btn_reserve.grid()
                    msg = "Available after\n" + self.bk_selected_due
                    self.lbl_action_display.config(text= msg)

                elif status[1] == "Reserved":
                    #Cannot Reserve
                    #Check whether the book is reserved by the current user
                    if self.bk_selected_id in self.user_reserved:
                        #Reserved by user -> can cancel;
                        # self.btn_cancel.config(state=tk.NORMAL)
                        # self.btn_cancel.grid()
                        self.lbl_action_display.config(text="You have\nreserved\nthis item")
                    else:
                        self.lbl_action_display.config(text="Item \nhas been\nreserved\nby another\nuser")     
        
    def on_borrow_btn_press(self):
        print(self.user_name," clicks borrows ",self.bk_selected_id)
        borrow_status = bkborrow.borrow_book(self.bk_selected_id,self.user_name)
        if borrow_status == "Borrowing succeeded": #Everything Ok
            print("Borrow Ok")
            self.user_borrowed.append(self.bk_selected_id)
            #Show borrow confirmation prompt
            msg = "You have borrowed " + self.bk_selected_title
            d1 = (datetime.today() + timedelta(days=28)).strftime("%d/%m/%Y")
            msg += "\n Due date is " + d1
            tk.messagebox.showinfo("Borrow Book",msg)
            #Update selection date
            self.bk_selected_due = d1
            #Refresh the ui
            self.update_local_tree("borrow")
        else:
            print("An error occured:")
            print(borrow_status)
        #Update buttons states
        self.switch_button_states(("On Loan","Not Reserved"))
    
    def on_reserve_btn_press(self):
        #print(self.user_name," clicks borrows ",self.bk_selected_id)
        reserve_status = bkborrow.reserve_book(self.bk_selected_id,self.user_name)
        if reserve_status == "Book reserved":
            print("Reserve Ok")
            #Show reserve confirmation prompt
            self.user_reserved.append(self.bk_selected_id)
            msg = "You have reserved " + self.bk_selected_title
            tk.messagebox.showinfo("Borrow Book",msg)
            #Refresh the ui
            self.update_local_tree("reserve")
        else:
            print("An error occured:")
            print(reserve_status)
        #Update buttons states
        self.switch_button_states(("Not Available","Reserved"))
            
        
    def update_local_tree(self,action):
        selected = self.treeview1.focus()
        old_vals = self.treeview1.item(selected,"values")
        if action == "borrow":
            new_vals = (old_vals[0],old_vals[1],"Not Available",old_vals[3])
        elif action == "reserve":
            new_vals = (old_vals[0],old_vals[1],old_vals[2],"Reserved")
        else:
            new_vals = old_vals
            print("ERROR: invalid action")
        
        self.treeview1.item(selected,text="",values=new_vals)

    ### HELPER FUNCTIONS ###

    def check_search_input(self):
        valid_input = False
        # Check search field
        if self.search_text.get() == "":
            self.lbl_msg_display.config(text="Fill in Search Request", fg="red")
        else:
            self.lbl_msg_display.config(text="", fg="green")
            valid_input = True
        return valid_input

    def search(self):
        search_words = self.search_text.get()
        if search_words != "":
            filt = self.drop.get()
            if filt == "Title":
                simple_search_dict = bksearch.simple_search(search_words)
                return bksearch.similarity_sort(simple_search_dict, search_words, "title")
            else:
                if filt == "ISBN" or filt == "Categories" or filt == "Authors":
                    #print(self.drop.get())
                    #print(self.sub_drop.get())
                    advance_search_dict = bksearch.advance_search(search_words, filt.lower())
                    return bksearch.similarity_sort(advance_search_dict, search_words, filt.lower())
                else:
                    filt = filt.replace(" ", "")
                    secondary_filt = self.sub_drop.get()
                    #print(self.drop.get())
                    #print(self.sub_drop.get())
                    #print(bksearch.advance_search(int(search_words),filt.lower(), secondary_filt.lower()))
                    return bksearch.advance_search(int(search_words), filt.lower(), secondary_filt.lower())
        else:
            return pd.DataFrame()


## DEBUG USE ONLY ###
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x600')
    root.minsize(600, 600)
    container = tk.Frame(root)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    
    test_user = {"userId": "henrychia07",
                 "unpaid_fines": False,
                 "borrowed": [79,308],
                 "reserved": []
                }
    
    frame = SearchDisplay(container,root,test_user)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.tkraise()
    
    root.mainloop()