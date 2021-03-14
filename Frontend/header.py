import tkinter as tk
from tkinter import ttk #we will use this later on...

HEADER_BG = "grey60"

def create_header(parent,username):
    frm_header_bar = tk.Frame(master=parent, bg = HEADER_BG)
    #Header bar is 1x3 grid
    for c in range(3):
        frm_header_bar.columnconfigure(c, weight=1)
    
    ## 1. Username Display 
    lbl_user = tk.Label(master=frm_header_bar,
                        text="Welcome " + username,
                        width=20,height=2)
    lbl_user.grid(row=0, column=0, padx=5,pady=10, sticky="nsw")
    
    ##3. Logout Button
    btn_logout = tk.Button(master=frm_header_bar, height=2, width=15,
                           text="Logout",
                           command = logout)
    btn_logout.grid(row=0, column=2, padx=5, pady=10, sticky="nse")

    return frm_header_bar

def logout():
    #TODO: handle logout
    pass

