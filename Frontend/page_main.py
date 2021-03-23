import tkinter as tk
from tkinter import ttk #we will use this later on...

HEADER_TOP_BG = "grey35"
HEADER_BTM_BG = "grey45"
HEADER_BTN = "grey69"

from page_home import HomePage
from page_searchdisplay import SearchDisplay
from page_payment import PaymentPage

class MainPage(tk.Frame):    
    def __init__(self, prev, parent, controller, session_user_data):
        super().__init__(parent)
        self.prev, self.parent, self.controller = prev,parent,controller
        #Set screen size etc
        controller.title("Library Application")
        controller.geometry("600x600")
        controller.minsize(600,600)
        
        ## Session variables ##
        self.user_data = session_user_data
    
        ## Initialize ##
        self.create_widgets()
    
    def create_widgets(self):
        ## Header Bar ##
        self.frm_header_bar = tk.Frame(master=self,bg=HEADER_TOP_BG)
        self.fill_header()
        self.frm_header_bar.pack(fill=tk.X)
        
        ### Content ###
        self.page_container = tk.Frame(master=self)
        self.page_container.pack(fill=tk.BOTH,expand=True)
        self.page_container.grid_rowconfigure(0, weight = 1)
        self.page_container.grid_columnconfigure(0, weight = 1)
        
        ## Initialize with HomePage
        self.current_page = HomePage(self.page_container,self,self.user_data)
        self.user_data = self.current_page.user_data
        self.current_page.grid(row=0,column=0,sticky="nsew")
        
        
    def fill_header(self):
        ### Top Row ###
        frm_top_row = tk.Frame(master=self.frm_header_bar,bg=HEADER_TOP_BG)
        frm_top_row.pack(fill=tk.X,expand=True)
        ## Username Display ##
        lbl_user = tk.Label(master=frm_top_row,text = "Welcome " + self.user_data["userId"], 
                            fg= "white", font=('', 12),
                            bg=HEADER_TOP_BG)
        lbl_user.pack(side=tk.LEFT,padx=(10,0),pady=5)
        
        ## Logout Button ##
        btn_logout = tk.Button(master=frm_top_row,padx=10,bg=HEADER_BTN,
                            text="Logout", command = self.on_logout_btn_press)
        btn_logout.pack(side=tk.RIGHT,padx=(0,10),pady=5)

        ### Bottom Row ###
        frm_btm_row = tk.Frame(master=self.frm_header_bar,bg=HEADER_TOP_BG)
        frm_btm_row.pack(pady=(0,5))
        for c in range(2):
            frm_btm_row.columnconfigure(c, weight=1)
        ## Manage/Home Button ##
        self.btn_home = tk.Button(master=frm_btm_row, width=10,
                            text="Manage",font=('', 11),
                            bg = HEADER_BTN, state=tk.DISABLED,
                            command = self.on_home_nav_btn_press)
        self.btn_home.grid(row=0, column=1, padx=20)
        
        ## Search Button ##
        self.btn_search = tk.Button(master=frm_btm_row,width=10,
                            text="Search",font=('', 11),
                            bg = HEADER_BTN,
                            command = self.on_search_nav_btn_press)
        self.btn_search.grid(row=0, column=2, padx=20)

    def on_home_nav_btn_press(self):
        self.current_page.destroy()
        # Display Home/Manage Page
        self.current_page = HomePage(self.page_container,self,self.user_data)
        self.user_data = self.current_page.user_data
        self.current_page.grid(row=0,column=0,sticky="nsew")
        self.btn_home.config(state=tk.DISABLED)
        self.btn_search.config(state=tk.NORMAL)
    
    def on_search_nav_btn_press(self):
        self.current_page.destroy()
        # Display Search Page
        self.current_page = SearchDisplay(self.page_container,self,self.user_data)
        self.current_page.grid(row=0,column=0,sticky="nsew")
        self.btn_home.config(state=tk.NORMAL)
        self.btn_search.config(state=tk.DISABLED)
        
    def on_pay_btn_press(self):
        self.btn_home.config(state=tk.DISABLED)
        self.btn_search.config(state=tk.DISABLED)
        # Display payments page (overlay over home)
        pay_page = PaymentPage(self.page_container,self,self.user_data)
        pay_page.grid(row=0,column=0,sticky="nsew")
        pay_page.tkraise()
        
    def refresh_home(self):
        self.on_home_nav_btn_press()    
        
    def on_logout_btn_press(self):
        #TODO: handle logout
        self.destroy()
        self.prev.refresh()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("600x600")
    root.minsize(600,600)
    container = tk.Frame(root)
    container.pack(side = "top", fill = "both", expand = True) 
    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)

    test_user = {"userId":"henrychia07"}

    frm_header_bar = MainPage(None,container,root,test_user)
    frm_header_bar.grid(row=0, column=0, sticky="nsew")
    root.mainloop()  

