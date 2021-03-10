import tkinter as tk
from tkinter import OptionMenu, ttk
from tkinter.constants import ACTIVE, DISABLED  # we will use this later on...
import BkSearch as bksearch
import pandas as pd

from header import create_header

options = {"Title": [], "ISBN": [], "Page Count": ["Lesser", "Equal", "Greater"],
           "Published Date": ["Before", "Equal", "After"], "Categories": [], "Authors": []}


class SearchDisplay(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent, self.controller = parent, controller
        controller.title("SearchDisplay")
        # Session Variables
        self.session_username = tk.StringVar()
        self.search_text = tk.StringVar(value="Search Catalogue")
        self.treedata = tk.StringVar()
        self.treedata.set("")

        ### DEVELOPMENT ONLY ###
        self.session_username.set("User")

        self.create_widgets()
        self.load_table1()

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
        frm_content.rowconfigure(2, weight=3)
        frm_content.pack(fill=tk.BOTH, pady=10, expand=True)

        # Some general styling vars
        HOME_CONTENT_PADX = 20

        ### Search ###
        frm_search = tk.Frame(master=frm_content, borderwidth=1)
        frm_search.grid(row=0, column=0, padx=HOME_CONTENT_PADX,
                        pady=(0, 10), sticky="nsew")

        ## Top row : Entry + Button ##
        frm_search_top = tk.Frame(master=frm_search)
        frm_search_top.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 0))

        # Search Entry #
        search_bar = tk.Entry(master=frm_search_top,
                              textvariable=self.search_text)
        search_bar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Search Button #
        btn_search = tk.Button(master=frm_search_top, text="Search", height=1, padx=5,
                               command=self.on_search_req_btn_press)
        btn_search.pack(side=tk.RIGHT, fill=tk.Y)

        # Error/Success Display
        self.lbl_msg_display = tk.Label(frm_search_top, text="", font=("", 10),
                                        height=None)
        self.lbl_msg_display.pack(pady=(0, 3))

        # Bottom row - Advanced search
        frm_search_btm = tk.Frame(master=frm_search)
        frm_search_btm.pack(fill=tk.X, expand=True, padx=10)

        # Drop Down Advanced Search #
        self.adv_dropdown = tk.StringVar()
        self.adv_dropdown.set("")
        self.drop = ttk.Combobox(
            frm_search_btm, values=list(options.keys()), state="readonly")
        self.drop.pack(side=tk.RIGHT, fill=tk.Y)

        # 2nd Bottom row - Sub Advanced search
        frm_search_btm_2 = tk.Frame(master=frm_search)
        frm_search_btm_2.pack(fill=tk.X, expand=True, padx=10)

        # Drop Down Sub Advanced Search #
        self.sub_adv_dropdown = tk.StringVar()
        self.sub_adv_dropdown.set("")
        self.sub_drop = ttk.Combobox(frm_search_btm_2, state="readonly")
        self.sub_drop.pack(side=tk.RIGHT, fill=tk.Y)

        self.drop.bind('<<ComboboxSelected>>', self.getUpdateData)

        #### Borrowed Books display ####
        # frm_borrowed = tk.Frame(master=frm_content, borderwidth=1, bg="red")
        # lbl_center = tk.Label(master=frm_borrowed,
        #                       text="Book Search Display", bg="red")
        # lbl_center.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        ### Treeview ###
        # browse - only 1 item can be selected
        frm_tree1 = tk.Frame(master=frm_content, borderwidth=1)
        tv = ttk.Treeview(frm_tree1, selectmode="browse")
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
        tv.column(HEADINGS[1], anchor='center',
                  width=300, minwidth=200, stretch=True)
        tv.column(HEADINGS[2], anchor='center',
                  width=100, minwidth=80, stretch=True)
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

        #### Book Details Display ####
        frm_bottom = tk.Frame(master=frm_content, bg="blue")

        frm_bottom.rowconfigure(0, weight=1)

        frm_bottom.columnconfigure(0, weight=3)
        frm_bkdetails = tk.Frame(master=frm_bottom, bg="yellow",
                                 relief=tk.RAISED, borderwidth=1)
        frm_bkdetails.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        #### Test Label ####
        self.lbl_show_info = tk.Label(
            master=frm_bkdetails, textvariable=self.treedata, bg="yellow")
        # lbl_show_info.grid(row=1, column=0)
        self.lbl_show_info.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        # Reserve Button #
        self.btn_reserve = tk.Button(master=frm_bkdetails, text="Reserve", height=1, padx=5, fg="White", bg="Blue",
                                     command=None)
        self.btn_reserve.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Borrow Button #
        self.btn_borrow = tk.Button(master=frm_bkdetails, text="Borrow", height=1, padx=5, fg="White", bg="green",
                                    command=None)
        self.btn_borrow.pack(side=tk.RIGHT, fill=tk.Y)

        ### Packing frame bottom ###
        # Add to layout
        frm_bottom.grid(row=2, column=0, padx=HOME_CONTENT_PADX,
                        pady=(10, 0), sticky="nsew")

    ### UI EVENT HANDLERS ###
    def getUpdateData(self,  event):
        self.sub_drop['values'] = options[self.drop.get()]

    def on_search_req_btn_press(self):
        if (not self.check_search_input()):
            return
        # Inputs valid:
        self.load_table1()

    def switch_bbutton_state(self):
        if self.treedata.get() != "":
            clicked_string_lst = self.treedata.get().split("|")
            if clicked_string_lst[2] != "Available":
                print(clicked_string_lst[2])
                self.btn_borrow.config(state=tk.DISABLED)
            else:
                self.btn_borrow.config(state=tk.NORMAL)
        else:
            self.btn_borrow.config(state=tk.NORMAL)

    def switch_rbutton_state(self):
        if self.treedata.get() != "":
            clicked_string_lst = self.treedata.get().split("|")
            if clicked_string_lst[3] != "Not Reserved":
                print(clicked_string_lst[3])
                self.btn_reserve.config(state=tk.DISABLED)
            else:
                self.btn_reserve.config(state=tk.NORMAL)
        else:
            self.btn_reserve.config(state=tk.NORMAL)

    def load_table1(self):
        search_df = self.search()
        self.treeview1.delete(*self.treeview1.get_children())
        for index, row in search_df.iterrows():
            self.treeview1.insert('', 'end', values=(
                index, row[0], row[1], row[2]))

    def on_tree_select(self, event):
        item = self.treeview1.selection()[0]
        # print('item:', item)
        # print('event:', event)
        text = "|".join(self.treeview1.item(item, 'values'))
        self.treedata.set(text)
        print(self.treedata.get())
        self.switch_bbutton_state()
        self.switch_rbutton_state()

    ### HELPER FUNCTIONS ###

    def check_search_input(self):
        valid_input = False
        # Check search field
        if self.search_text.get() == "" or self.search_text.get() == "Search Catalogue":
            self.lbl_msg_display.config(
                text="Fill in Search Request", fg="red")
        else:
            valid_input = True
        return valid_input

    def search(self):
        search_words = self.search_text.get()
        if search_words != "" and search_words != "Search Catalogue":
            filt = self.drop.get()
            if filt == "":
                simple_search_dict = bksearch.simple_search(search_words)
                return bksearch.similarity_sort(
                    simple_search_dict, search_words, "title")
            else:
                if filt == "Title" or filt == "ISBN" or filt == "Categories" or filt == "Authors":
                    # print(self.drop.get())
                    # print(self.sub_drop.get())
                    advance_search_dict = bksearch.advance_search(
                        search_words, filt.lower())
                    return bksearch.similarity_sort(
                        advance_search_dict, search_words, filt.lower())
                else:
                    filt = filt.replace(" ", "")
                    secondary_filt = self.sub_drop.get()
                    # print(self.drop.get())
                    # print(self.sub_drop.get())
                    # print(bksearch.advance_search(int(search_words),filt.lower(), secondary_filt.lower()))
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
    frame = SearchDisplay(container, root)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.tkraise()
    root.mainloop()
