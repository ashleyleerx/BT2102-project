# pylint: disable=E1101
from tkinter import Toplevel, Label, Button, StringVar, Entry
    
class NewLoginWindow(Toplevel): 
    def __init__(self, master): 
        Toplevel.__init__(self,master)
        self.title("Login")
        self.geometry("300x250") 
        # Set text variables
        self.username = StringVar()
        self.password = StringVar()
        self.create_widgets()
        
    def spacer(self):
        Label(self, text="").pack()
    
    def create_widgets(self):
        #Header Label for user's instruction
        Label(self, text="Login", bg="#F0F8FF").pack()
        self.spacer()
    
        # Username entry
        # Note: The Entry widget is a standard Tkinter widget used to enter or
        # display a single line of text.
        username_entry = Entry(self, textvariable=self.username)
        self.username.set("username") #sets the text in entry field
        username_entry.pack()
        self.spacer()
        
        # Password entry
        password_entry = Entry(self, textvariable=self.password, show='*')
        self.password.set("password")
        password_entry.pack()
        self.spacer()
        
        # Login button   
        Button(self, text="Login", width=10, height=1,
            command = self.check_login).pack()
        self.spacer()
    
    # on press of login
    def check_login(self):
        #Do something 
        Label(self, text="Login Success", fg="green", font=("calibri", 11)).pack()
        Label(self, text="Please wait for a moment", fg="green", font=("calibri", 11)).pack()
        self.master.updateUserName(self.username.get())
        self.after(2000,self.destroy)
        
    