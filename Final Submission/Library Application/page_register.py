import tkinter as tk
from login import check_credential, create_account

class RegisterPage(tk.Frame): 
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent,self.controller = parent, controller
        
        # Text Variables
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        ## Content Container ##
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        frm_content = tk.Frame(master = self)       
        frm_content.grid(row=0,column=0,sticky="")  
        
        #Header Label for user's instruction
        tk.Label(frm_content, text="Register",font=("", 20)).pack()
    
        frm_reg_form = tk.Frame(frm_content)
        frm_reg_form.pack(pady=(10,0))
        frm_reg_form.columnconfigure(0,weight=4)
        frm_reg_form.columnconfigure(1,weight=6)
        
        ## Username ##
        frm_reg_form.rowconfigure(0,weight=1)
        tk.Label(frm_reg_form, text="New username",height=1).grid(row=0,column=0,sticky="e",pady=(0,10))
        ent_username = tk.Entry(frm_reg_form, textvariable=self.username)
        ent_username.grid(row=0,column=1,sticky="",pady=(0,10))
        
        ## Password ##
        frm_reg_form.rowconfigure(1,weight=1)
        tk.Label(frm_reg_form, text="New password",height=1).grid(row=1,column=0,sticky="e")
        ent_password = tk.Entry(frm_reg_form, textvariable=self.password, show='*')
        ent_password.grid(row=1,column=1,sticky="")
        
        ## Message display ## - Create but do not grid yet
        self.lbl_msg_disp = tk.Label(frm_reg_form,text="")
        
        ## Register button ## 
        self.btn_reg = tk.Button(frm_content, text="Create Account",height=1, width=12,
                                 bg="lightblue",activebackground="lightblue",
                                 command = self.on_create_account_btn_press)
        self.btn_reg.pack(pady=(15,0))
        
        ## Cancel button ##
        self.btn_cancel = tk.Button(frm_content, text="Cancel",height=1, width=12,
                                 bg="crimson",activebackground="crimson",
                                 command = self.on_cancel_btn_press)
        self.btn_cancel.pack(pady=(5,20))
    
    ## UI event handler
    def on_create_account_btn_press(self):
        # Push the message display (if not exists)
        if (not self.lbl_msg_disp.winfo_ismapped()):
            self.lbl_msg_disp.grid(row=2,column=0,columnspan=2,sticky="",pady=(5,0))
            self.btn_reg.pack_configure(pady=(5,5))
        
        #Get fields from Entry(s)
        username,password = self.username.get(), self.password.get()
        # Check inputs
        if (not self.check_input(username,password)): 
            return 
        #Inputs valid:
        self.doRegister(username,password)
        
    def on_cancel_btn_press(self):
        self.destroy()

    def check_input(self,username,password):
        valid_input = False
        #Check username field
        if username == "": 
            self.lbl_msg_disp.config(text="Fill in Username", fg = "red")
        elif len(username) > 25:
            self.lbl_msg_disp.config(text="Username too long", fg = "red")
        #Check password field
        elif password == "":
            self.lbl_msg_disp.config(text="Fill in Password", fg = "red")
        elif len(password) > 25:
            self.lbl_msg_disp.config(text="Password too long", fg = "red")
        else:
            valid_input = True
        return valid_input
    
    def doRegister(self,username,password):
        #Check credentials
        status = check_credential(username,password)
        if status == 3: #account does not exist, create
            rsp = create_account(username,password)
            if rsp == "Success. New User Created!":
                self.lbl_msg_disp.config(text="Account Sucessfully Created \nPlease Login",fg="green")
                self.master.after(1500,self.destroy)
            else: #some error 
                self.lbl_msg_disp.config(test="ERROR",fg="red")
        else:
            self.lbl_msg_disp.config(text="Username Taken \nPlease try again",fg="red")
                