import tkinter as tk
from tkinter import ttk 

#from login import check_credential
from window_register import RegisterWindow
    
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
        frm_login.pack(pady=5)
        
        #Username
        tk.Label(frm_login, text="Username",
                 width=15,height=1).pack()
        ent_login_username = tk.Entry(frm_login,textvariable=self.session_username)
        ent_login_username.pack(pady=(0,10))
        
        #Password
        tk.Label(frm_login, text="Password",
                 width=15,height=1).pack()
        ent_login_password = tk.Entry(frm_login,textvariable=self.session_password,show = "*")
        ent_login_password.pack(pady=(0,5))  
        
        #Error/Success Display
        self.lbl_msg_display = tk.Label(frm_login, text= "", font=("", 10),
                                        height=None)
        self.lbl_msg_display.pack(pady = (0,3))
        
        #Login Button
        btn_login = tk.Button(frm_login, text="Login",width=10,height=1, borderwidth=2, 
                              bg="lightblue",activebackground="lightblue",
                              command = self.on_login_btn_press)
        btn_login.pack(pady=(0,10))
        
        ## Register Container ##
        frm_reg = tk.Frame(frm_content,borderwidth=1,relief=tk.FLAT)
        # Register message label
        lbl_reg = tk.Label(frm_reg,text="For new users: ", height=1)
        lbl_reg.pack(side=tk.LEFT)        
        # #Register Button
        btn_register = tk.Button(frm_reg, text="Register",
                                 width=8,height=1, relief=tk.GROOVE,
                                 command=self.on_register_btn_press)
        btn_register.pack(side=tk.LEFT)
        # layout Container 
        frm_reg.pack(pady=(0,20))
        
    
    ### UI EVENT HANDLERS ###
    def on_login_btn_press(self):
        if (not self.check_input()): 
            return 
        #Inputs valid:
        self.login()
        
    def on_register_btn_press(self):
        #Launch Register window
        self.newRegisterWindow = RegisterWindow(self.controller)
            
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
root.geometry('300x300')
root.minsize(300,300)
container = tk.Frame(root)
container.pack(side = "top", fill = "both", expand = True) 
container.grid_rowconfigure(0, weight = 1)
container.grid_columnconfigure(0, weight = 1)
frame = LoginPage(container,root)
frame.grid(row = 0, column = 0, sticky ="nsew")
frame.tkraise()
root.mainloop()  