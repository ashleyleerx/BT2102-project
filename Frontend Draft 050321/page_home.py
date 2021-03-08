import tkinter as tk
from tkinter import ttk  # we will use this later on...
import BkSearch as bksearch

from header import create_header


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent, self.controller = parent, controller
        controller.title("Homepage")
        # Session Variables
        self.session_username = tk.StringVar()
        self.user_fines = tk.DoubleVar()
        self.search_text = tk.StringVar(value="Search Catalogue")

        ### DEVELOPMENT ONLY ###
        self.session_username.set("User")
        self.user_fines.set(69.69)

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
        # Advanced Search button #
        btn_adv_search = tk.Button(master=frm_search_btm, text="Advanced Search",
                                   height=1, relief=tk.GROOVE)
        btn_adv_search.pack(side=tk.RIGHT)

        #### Borrowed Books display ####
        frm_borrowed = tk.Frame(master=frm_content, borderwidth=1, bg="red")
        lbl_center = tk.Label(master=frm_borrowed,
                              text="Borrowed books", bg="red")
        lbl_center.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        # Add to layout
        frm_borrowed.grid(
            row=1, column=0, padx=HOME_CONTENT_PADX, sticky="nsew")

        #### Reserved Books and Pay Fines Display ####
        frm_bottom = tk.Frame(master=frm_content, bg="blue")
        # bottom frame is 1x2 grid - consists of following elements:
        frm_bottom.rowconfigure(0, weight=1)
        # Reserved Books Display: 75% size
        frm_bottom.columnconfigure(0, weight=3)
        frm_reserved = tk.Frame(master=frm_bottom, bg="yellow",
                                relief=tk.RAISED, borderwidth=1)
        frm_reserved.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        lbl_reserved = tk.Label(master=frm_reserved,
                                text="Reserved books", bg="yellow")
        lbl_reserved.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        # Fines Display: 25% size
        frm_bottom.columnconfigure(1, weight=1)
        frm_fines = tk.Frame(master=frm_bottom, bg="green",
                             relief=tk.RAISED, borderwidth=1)
        frm_fines.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Sub-Container
        frm_fines.grid_rowconfigure(0, weight=1)
        frm_fines.grid_columnconfigure(0, weight=1)
        frm_fines_c = tk.Frame(master=frm_fines, bg="pink")

        # Info text
        lbl_fine_txt = tk.Label(
            master=frm_fines_c, text="Fines payable", font=('', 12))
        lbl_fine_txt.pack(fill=tk.X)
        # Show fine amount
        lbl_fine_amt = tk.Label(master=frm_fines_c, text="$" + str(self.user_fines.get()),
                                foreground="red", font=('', 12))
        lbl_fine_amt.pack(fill=tk.X)
        # Pay fines button
        btn_pay_fine = tk.Button(master=frm_fines_c, text="Pay")
        btn_pay_fine.pack(fill=tk.X)
        # TO-DO fancy highlighting thing

        frm_fines_c.grid(row=0, column=0, sticky="", ipadx=10, ipady=10)

        ### Packing frame bottom ###
        # Add to layout
        frm_bottom.grid(row=2, column=0, padx=HOME_CONTENT_PADX,
                        pady=(10, 0), sticky="nsew")

    ### UI EVENT HANDLERS ###

    def on_search_req_btn_press(self):
        if (not self.check_search_input()):
            return
        # Inputs valid:
        self.simplesearch()

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

    def simplesearch(self):
        simple_search_words = self.search_text.get()
        simple_search_dict = bksearch.simple_search(simple_search_words)
        print(bksearch.similarity_sort(
            simple_search_dict, simple_search_words, "title"))


## DEBUG USE ONLY ###
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x600')
    root.minsize(600, 600)
    container = tk.Frame(root)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    frame = HomePage(container, root)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.tkraise()
    root.mainloop()
