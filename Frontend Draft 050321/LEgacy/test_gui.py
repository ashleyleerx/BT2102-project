import tkinter as tk
#from tkinter.ttk import *

from login_window import *

class GUI(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master 
        #Session Variables
        self.session_username = tk.StringVar()
        #Populate window with widgets
        self.create_widgets()
        
    def create_widgets(self):
        loginButton = tk.Button(text="Login",width=25,height=5)
        loginButton.bind("<Button>", lambda e: NewLoginWindow(self)) 
        loginButton.pack()
        
        self.session_username.set("default_user")
        tk.Label(textvariable=self.session_username,width=10,height=1).pack()
        
    #Helper methods
    
    def updateUserName(self,inputUser):
        self.session_username.set(inputUser)

#Driver Functions
root = tk.Tk()
myapp = GUI(root)
root.geometry('600x400')
root.mainloop()