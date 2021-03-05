import tkinter as tk
from tkinter import ttk #we will use this later on...
    
HEADER_BG = "grey60"

SAMPLE_DATA = [(1,"Unlocking Android"),
               (2,"Android in Action, Second Edition"),
               (3,"Specification by Example"),
               (4,"Flex 3 in Action"),
               (5,"Flex 4 in Action"),
               (5,"Flex 4 in Action"),
               (5,"Flex 4 in Action"),
               (5,"Flex 4 in Action"),
               (5,"Flex 4 in Action"),
               (5,"Flex 4 in Action"),
               (5,"Flex 4 in Action"),
               (5,"Flex 4 in Action"),
               (5,"Flex 4 in Action"),
               (5,"Flex 4 in Action"),
               ]

class TreeTest(tk.Frame):    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent,self.controller = parent, controller 
        controller.title("TreeTest")
        #Session Variables
        #self.session_username = tk.StringVar()
        self.treedata = tk.StringVar()
        self.treedata.set("test")
        
        self.create_widgets()
        self.load_table1()
        
    def create_widgets(self):
        """
        Use the following widget abbreviations
        Label 	 lbl 	lbl_name
        Button 	 btn 	btn_submit
        Entry 	 ent 	ent_age
        Text 	 txt 	txt_notes
        Frame 	 frm 	frm_address
        TreeView tv     tv_books
        """
        
        #### Frame for Treeview & Scrollbar ####
        frm_tree1 = tk.Frame(self)

        ### Treeview ###
        tv = ttk.Treeview(frm_tree1, selectmode = "browse") #browse - only 1 item can be selected
        tv.pack(side="left")

        ## Configure Treeview ##
        HEADINGS = ('Id', 'Title', 'Status', 'Expected due date')
        tv['columns'] = HEADINGS
        tv["show"] = "headings" #supresses icon(#0) column
        # tv.heading("#0", text='Sources', anchor='w')
        # tv.column("#0", anchor="w")
        
        #Set headings (column names)
        for h in HEADINGS: 
            tv.heading(h, text=h)
        #Set column sizing 
        tv.column(HEADINGS[0], anchor='e', width=40, minwidth=40,stretch= False)
        tv.column(HEADINGS[1], anchor='center', width=200, minwidth=200, stretch=False)
        tv.column(HEADINGS[2], anchor='center', width=80, minwidth=80, stretch= False)
        tv.column(HEADINGS[3], anchor='center', width=40, stretch= False)
        
        #Bind event handlers
        # single click, without "index out of range" error
        tv.bind("<<TreeviewSelect>>", self.on_tree_select)

        ## Scrollbar for Treeview ##
        tvScroll = ttk.Scrollbar(frm_tree1, orient="vertical", command=tv.yview) 
        tv.configure(yscrollcommand=tvScroll.set)
        tvScroll.pack(side="right",fill='y')
        
        #Assign treeview
        self.treeview1 = tv
        
        ### Layout frame ###
        self.grid_columnconfigure(0, weight=1)
        frm_tree1.grid(row=0,column=0,sticky = "nsew")
        
        #### Test Label ####
        lbl_show_info = tk.Label(self, textvariable = self.treedata)
        lbl_show_info.grid(row=1,column=0)
        
    def load_table1(self):
        for row in SAMPLE_DATA:
            self.treeview1.insert('', 'end', values= row + ("Available","-"))
            
    def on_tree_select(self,event):
        item = self.treeview1.selection()[0]
        #print('item:', item)
        #print('event:', event)
        text = "|".join(self.treeview1.item(item,'values'))
        self.treedata.set(text)
        
    
        
        
        
    

        
        
### DEBUG USE ONLY ###
root = tk.Tk()
root.geometry('400x400')
root.minsize(400,400)
container = tk.Frame(root)
container.pack(side = "top", fill = "both", expand = True) 
container.grid_rowconfigure(0, weight = 1)
container.grid_columnconfigure(0, weight = 1)
frame = TreeTest(container,root)
frame.grid(row = 0, column = 0, sticky ="nsew")
frame.tkraise()
root.mainloop()  