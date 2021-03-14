import tkinter as tk
#from tkinter.ttk import *

from page_login import LoginPage
from page_home import HomePage

class Application(tk.Tk):
    #Tuple of tk.Frames; represents all our pages
    PAGES = (("Login",LoginPage),("Home",HomePage))
    GEO = '300x300'
    MINSIZE = (300,300)
    
    
    def __init__(self, *args, **kwargs): 
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        
        # sizing
        self.geometry(self.GEO)
        self.minsize(*self.MINSIZE)
        
        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.container = container
  
        # initializing frames to an empty array
        self.frames = {}  
  
        # iterating through a tuple consisting of the different page layouts
        for fName, F in self.PAGES:
            # initializing frame of that object
            frame = F(container, self)
            self.frames[fName] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")
    
        print(self.frames)
        self.show_frame(self.PAGES[0])
  
    # Helper Methods
    # Displays the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont[0]]
        frame.tkraise()

#Driver Functions
root = Application()
root.mainloop()