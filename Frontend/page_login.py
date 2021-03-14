import tkinter as tk
from tkinter import ttk 

#from login import check_credential
from page_register import RegisterPage
from page_admin import AdminLoginPage
    
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
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
        tk.Label(frm_content, text = "Library System", font=("Times", 25)).pack()
        
        ## Login Form Container ##
        frm_login = tk.Frame(frm_content)
        frm_login.pack(pady=(10,0))
        
        #Username
        tk.Label(frm_login, text="Username",
                 width=15,height=1).pack()
        ent_login_username = tk.Entry(frm_login, width=20,
                                      textvariable=self.session_username)
        ent_login_username.pack(pady=(0,10))
        
        #Password
        tk.Label(frm_login, text="Password",
                 width=15,height=1).pack()
        ent_login_password = tk.Entry(frm_login,width=20,
                                      textvariable=self.session_password,show = "*")
        ent_login_password.pack()  
        
        ## Message display ## - Create but do not grid yet
        self.lbl_msg_display = tk.Label(frm_login, text= "", bg="red")
        
        #Login Button
        self.btn_login = tk.Button(frm_content, text="Login",width=10,height=1, borderwidth=2, 
                                   bg="lightblue",activebackground="lightblue",
                                   command = self.on_login_btn_press)
        self.btn_login.pack(pady=(15,0))
        
        ### Other Button Container ###
        frm_others = tk.Frame(frm_content,borderwidth=1,relief=tk.FLAT)
        frm_others.pack(pady=(25,20))
    
        # Register message label
        lbl_reg = tk.Label(frm_others,text="For new users: ", height=1)
        lbl_reg.grid(row=0,column=0,pady=(0,5),sticky="nsw")        
        # #Register Button
        btn_register = tk.Button(frm_others, text="Register",
                                 width=10,height=1, relief=tk.GROOVE,
                                 command=self.on_register_btn_press)
        btn_register.grid(row=0,column=1,pady=(0,5))
        
        # Admin Login message label
        lbl_adm = tk.Label(frm_others,text="For admins: ", height=1)
        lbl_adm.grid(row=1,column=0,sticky="nsw")        
        # Admin Login Button
        btn_adm = tk.Button(frm_others, text="Admin Login",
                                 width=10,height=1, relief=tk.GROOVE,
                                 command=self.on_admin_btn_press)
        btn_adm.grid(row=1,column=1)
    
    
    ### UI EVENT HANDLERS ###
    def on_login_btn_press(self):
        if (not self.lbl_msg_display.winfo_ismapped()):
            self.lbl_msg_display.pack(pady=(5,0))
            self.btn_login.pack_configure(pady=(5,0))
        
        if (not self.check_input()): 
            return 
        #Inputs valid:
        self.login()
        
    def on_register_btn_press(self):
        #Launch Register window
        print("regista!")
        nextPage = RegisterPage(self.parent,self.controller)
        # print(nextPage)
        nextPage.grid(row = 0, column = 0, sticky ="nsew")
        nextPage.tkraise()
        
    def on_admin_btn_press(self):
        nextPage = AdminLoginPage(self.parent,self.controller)
        nextPage.grid(row = 0, column = 0, sticky ="nsew")
        nextPage.tkraise()
            
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
        #status = check_credential(usr_n,pw)
        
        """ TESTING ONLY """
        status = 1
        
        ## Update Page based on status ##
        login_ok = False 
        if status == 1: #ID and password match, Login ok
            self.lbl_msg_display.config(text="Login Sucessful", fg = "green")
            login_ok = True
        elif status == 2: #ID match but wrong password
            self.lbl_msg_display.config(text="Incorrect Password. Please Try Again", fg = "red")
        elif status == 3: #Invalid username
            self.lbl_msg_display.config(text="Invalid Username. Please Try Again", fg = "red")
        
        ## Process Sucessful Login ##
        #TODO: 
        if login_ok: 
            pass
        # SIMPLE METHOD OF SETTING - PROBABLY NOT THE BEST SECURITY WISE #
        #nextPage = self.controller.PAGES[1]
        #self.controller.show_frame(nextPage)
            
## DEBUG USE ONLY ###
root = tk.Tk()
root.geometry('400x400')
root.minsize(300,300)
container = tk.Frame(root)
container.pack(side = "top", fill = "both", expand = True) 
container.grid_rowconfigure(0, weight = 1)
container.grid_columnconfigure(0, weight = 1)
frame = LoginPage(container,root)
frame.grid(row = 0, column = 0, sticky ="nsew")
frame.tkraise()
root.mainloop()  