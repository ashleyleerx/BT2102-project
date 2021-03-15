import tkinter as tk
from tkinter import ttk  # we will use this later on...
import pandas as pd
from GetViews import admin_view_bksborrowed, admin_view_unpaidfines, admin_view_bksreserved

from header import create_header

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent, self.controller = parent, controller
        controller.title("AdminPage")
        # Session Variables
        self.session_username = tk.StringVar()

        ### DEVELOPMENT ONLY ###
        self.session_username.set("Admin")

        self.create_widgets()
        self.borrow_books_table()
        self.admin_fines_table()
        self.reserve_books_table()

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
        frm_header_bar = create_header(self, self.session_username.get())
        frm_header_bar.pack(fill=tk.X)

        #### Page Content ####
        frm_content = tk.Frame(master=self)
        frm_content.columnconfigure(0, weight=1)
        frm_content.rowconfigure(0, weight=1)
        frm_content.rowconfigure(1, weight=10)
        frm_content.rowconfigure(2, weight=1)
        frm_content.rowconfigure(3, weight=10)
        frm_content.rowconfigure(4, weight=1)
        frm_content.rowconfigure(5, weight=10)
        frm_content.pack(fill=tk.BOTH, pady=10, expand=True)

        # Some general styling vars
        HOME_CONTENT_PADX = 20

        ##Borrowed Books Title##
        frm_borrowed = tk.Frame(master=frm_content, borderwidth=2, bg="pink")
        lbl_center = tk.Label(master=frm_borrowed,
                              text="Borrowed books", bg="pink")
        lbl_center.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        # Add to layout
        frm_borrowed.grid(
            row=0, column=0, padx=HOME_CONTENT_PADX, sticky="nsew")
        
        #### Borrowed Books display ####
        ### Treeview ###
        # browse - only 1 item can be selected
        frm_tree1 = tk.Frame(master=frm_content, borderwidth=1)
        tv = ttk.Treeview(frm_tree1, selectmode="browse")
        tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ## Configure Treeview ##
        HEADINGS = ('Book ID', 'Book Title', 'Borrow Member ID', 'Duedate')
        tv['columns'] = HEADINGS
        tv["show"] = "headings"  # supresses icon(#0) column
        # tv.heading("#0", text='Sources', anchor='w')
        # tv.column("#0", anchor="w")

        # Set headings (column names)
        for h in HEADINGS:
            tv.heading(h, text=h)
        # Set column sizing
        tv.column(HEADINGS[0], anchor='center', width=120,
                  minwidth=100, stretch=True)
        tv.column(HEADINGS[1], anchor='center',
                  width=150, minwidth=120, stretch=True)
        tv.column(HEADINGS[2], anchor='center',
                  width=120, minwidth=110, stretch=True)
        tv.column(HEADINGS[3], anchor='center', width=100, stretch=True)

        # Bind event handlers
        # single click, without "index out of range" error
        tv.bind("<<TreeviewSelect>>", self.on_tree_select)

        ## Scrollbar for Treeview ##
        tvScroll = ttk.Scrollbar(
            frm_tree1, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=tvScroll.set)
        tvScroll.pack(side="right", fill='y')

        # Assign treeview
        self.treeview1 = tv

        # Add to layout
        frm_tree1.grid(
            row=1, column=0, padx=HOME_CONTENT_PADX, sticky="nsew")

        ## Reserved Books Title##
        frm_reserved = tk.Frame(master=frm_content, borderwidth=1, bg="pink")
        lbl_center = tk.Label(master=frm_reserved,
                              text="Reserved books", bg="pink")
        lbl_center.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        # Add to layout
        frm_reserved.grid(
            row=2, column=0, padx=HOME_CONTENT_PADX, sticky="nsew")

        
        #### Reserved Books display ####
        ### Treeview ###
        # browse - only 1 item can be selected
        frm_tree2 = tk.Frame(master=frm_content, borderwidth=1)
        tv = ttk.Treeview(frm_tree2, selectmode="browse")
        tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ## Configure Treeview ##
        HEADINGS = ('Book ID', 'Book Title', 'Reserve Member ID')
        tv['columns'] = HEADINGS
        tv["show"] = "headings"  # supresses icon(#0) column
        # tv.heading("#0", text='Sources', anchor='w')
        # tv.column("#0", anchor="w")

        # Set headings (column names)
        for h in HEADINGS:
            tv.heading(h, text=h)
        # Set column sizing
        tv.column(HEADINGS[0], anchor='center', width=100,
                  minwidth=120, stretch=True)
        tv.column(HEADINGS[1], anchor='center',
                  width=120, minwidth=100, stretch=True)
        tv.column(HEADINGS[2], anchor='center',
                  width=120, minwidth=100, stretch=True)
        

        # Bind event handlers
        # single click, without "index out of range" error
        tv.bind("<<TreeviewSelect>>", self.on_tree_select)

        ## Scrollbar for Treeview ##
        tvScroll = ttk.Scrollbar(
            frm_tree2, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=tvScroll.set)
        tvScroll.pack(side="right", fill='y')

        # Assign treeview
        self.treeview2 = tv

        # Add to layout
        frm_tree2.grid(
            row=3, column=0, padx=HOME_CONTENT_PADX, sticky="nsew")

        ##Fines Title##
        frm_fines = tk.Frame(master=frm_content, borderwidth=1, bg="pink")
        lbl_center = tk.Label(master=frm_fines,
                              text="Fines", bg="pink")
        lbl_center.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        # Add to layout
        frm_fines.grid(
            row=4, column=0, padx=HOME_CONTENT_PADX, sticky="nsew")
        
        #### Fines display ####
        ### Treeview ###
        # browse - only 1 item can be selected
        frm_tree3 = tk.Frame(master=frm_content, borderwidth=1)
        tv = ttk.Treeview(frm_tree3, selectmode="browse")
        tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ## Configure Treeview ##
        HEADINGS = ('Index', 'Member ID', 'Fine Amount', 'Fine Date')
        tv['columns'] = HEADINGS
        tv["show"] = "headings"  # supresses icon(#0) column
        # tv.heading("#0", text='Sources', anchor='w')
        # tv.column("#0", anchor="w")

        # Set headings (column names)
        for h in HEADINGS:
            tv.heading(h, text=h)
            
        # Set column sizing
        tv.column(HEADINGS[0], anchor='center', width=120,
                  minwidth=100, stretch=True)
        tv.column(HEADINGS[1], anchor='center',
                  width=150, minwidth=120, stretch=True)
        tv.column(HEADINGS[2], anchor='center',
                  width=120, minwidth=110, stretch=True)
        tv.column(HEADINGS[3], anchor='center', width=100, stretch=True)

        # Bind event handlers
        # single click, without "index out of range" error
        tv.bind("<<TreeviewSelect>>", self.on_tree_select)

        ## Scrollbar for Treeview ##
        tvScroll = ttk.Scrollbar(
            frm_tree3, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=tvScroll.set)
        tvScroll.pack(side="right", fill='y')

        # Assign treeview
        self.treeview3 = tv

        # Add to layout
        frm_tree3.grid(
            row=5, column=0, padx=HOME_CONTENT_PADX, sticky="nsew")
        
        
    ### UI EVENT HANDLERS ###
    def borrow_books_table(self):
        borrowed_books_df = admin_view_bksborrowed()
        self.treeview1.delete(*self.treeview1.get_children())
        for index, row in borrowed_books_df.iterrows():
            self.treeview1.insert('', 'end', values=(
                row[0], row[1], row[2], row[3]))
       
    def reserve_books_table(self):
        reserve_books_df = admin_view_bksreserved()
        self.treeview2.delete(*self.treeview2.get_children())
        for index, row in reserve_books_df.iterrows():
            self.treeview2.insert('', 'end', values=(row[0], row[1], row[2]))
    
    def admin_fines_table(self):
        fines_df = admin_view_unpaidfines()
        self.treeview3.delete(*self.treeview3.get_children())
        for index, row in fines_df.iterrows():
            self.treeview3.insert('', 'end', values=(
                index + 1, row[0], row[1], row[2]))

            
    def on_tree_select(self, event):
        item = self.treeview1.selection()[0]
        # print('item:', item)
        # print('event:', event)
        text = "|".join(self.treeview1.item(item, 'values'))
        #self.treedata.set(text)
        #print(self.treedata.get())
        #self.switch_bbutton_state()
        #self.switch_rbutton_state()

## DEBUG USE ONLY ###
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x600')
    root.minsize(600, 600)
    container = tk.Frame(root)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    frame = AdminPage(container, root)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.tkraise()
    root.mainloop()
