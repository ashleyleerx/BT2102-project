import tkinter as tk
from tkinter import ttk 

from AdminLogin import check_credential
from page_admin_view import AdminPage
    
class AdminLoginPage(tk.Frame):
    def __init__(self,prev, parent, controller):
        super().__init__(parent)
        self.prev = prev
        self.parent,self.controller = parent, controller
        #Session Variables
        self.session_username = tk.StringVar()
        self.session_password = tk.StringVar()
        #Register Variables
        self.session_register = tk.StringVar()
        
        #Window
        self.newRegisterWindow = None
        
        #Populate window with widgets
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
        
        ### Content Container ###
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        frm_content = tk.Frame(master = self)
        frm_content.grid(row=0,column=0, sticky="")

        #Logo Display
        tk.Label(frm_content, text = "Admin Login", font=("Times", 20)).pack()
        
        ## Login Form Container ##
        frm_login = tk.Frame(frm_content)
        frm_login.pack()
        
        #Username
        tk.Label(frm_login, text="Username",
                 width=15,height=1).pack()
        ent_login_username = tk.Entry(frm_login,textvariable=self.session_username)
        ent_login_username.pack(pady=(0,10))
        
        #Password
        tk.Label(frm_login, text="Password",
                 width=15,height=1).pack()
        ent_login_password = tk.Entry(frm_login,textvariable=self.session_password,show = "*")
        ent_login_password.pack()  
        
        ## Message display ## - Create but do not grid yet
        self.lbl_msg_display = tk.Label(frm_login, text= "")
        
        #Login Button
        self.btn_login = tk.Button(frm_content, text="Login",width=10,height=1, borderwidth=2, 
                                   bg="lightblue",activebackground="lightblue",
                                   command = self.on_login_btn_press)
        self.btn_login.pack(pady=(15,0))
        
        ## Cancel button ##
        self.btn_cancel = tk.Button(frm_content, text="Cancel",height=1, width=10,
                                 bg="crimson",activebackground="crimson",
                                 command = self.on_cancel_btn_press)
        self.btn_cancel.pack(pady=(5,20))
    
    def refresh(self):
        # Windowing
        self.controller.geometry('400x400')
        self.controller.minsize(300,300)
        # Widget Settings
        if (self.lbl_msg_display.winfo_ismapped()):
            self.lbl_msg_display.pack_forget()
            self.btn_login.pack_configure(pady=(15,0))
        self.session_username.set("")
        self.session_password.set("")
    
    ### UI EVENT HANDLERS ###
    def on_login_btn_press(self):
        if (not self.lbl_msg_display.winfo_ismapped()):
            self.lbl_msg_display.pack(pady=(5,0))
            self.btn_login.pack_configure(pady=(5,0))
        if (not self.check_input()): 
            return 
        #Inputs valid:
        self.login()
        
    def on_cancel_btn_press(self):
        self.destroy()
            
    ### HELPER FUNCTIONS ###
    def check_input(self):
        valid_input = False
        #Check username field
        if self.session_username.get() == "": 
            self.lbl_msg_display.config(text="Fill in Username", fg = "red")
        #Check password field
        elif self.session_password.get() == "":
            self.lbl_msg_display.config(text="Fill in Password", fg = "red")
        else:
            valid_input = True
        return valid_input
        
        
    def login(self): 
        ## Verify User Credentials ##
        usr_n, pw = self.session_username.get(), self.session_password.get()
        
        # Calls backend method - returns an integer 
        status = check_credential(usr_n,pw)
        
        ## Update Page based on status ##
        login_ok = False 
        if status == "Login Successful": #ID and password match, Login ok
            self.lbl_msg_display.config(text="Login Sucessful", fg = "green")
            login_ok = True
        elif status == "Login Unsuccessful -- Incorrect Password": #ID match but wrong password
            self.lbl_msg_display.config(text="Incorrect Password. Please Try Again", fg = "red")
        elif status == "User not found": #Invalid username
            self.lbl_msg_display.config(text="Invalid Username. Please Try Again", fg = "red")
        else:
            self.lbl_msg_display.config(text="ERROR", fg = "red")
        
        ## Process Sucessful Login ##
        #TODO: 
        if login_ok:
            nextPage = AdminPage(self,self.parent,self.controller,{"userId": usr_n})
            nextPage.grid(row=0, column=0, sticky="nsew")
            