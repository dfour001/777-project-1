import tkinter as tk
from tkinter import Frame, Label

class ProgressBar(Frame):
    """ A custom widget based on the Frame class that displays a progress bar and status text """
    def __init__(self, root, initProgress = 0.75):
        super().__init__(root)

        # Display progress bar frame
        self.frameProgress = Frame(root, bg="black", bd=5, relief=tk.RIDGE)
        self.frameProgress.place(relheight=0.2, relwidth=0.5, relx=0.25, rely=0.4)
        self.frameProgress.focus() # Just to make the entry box lose focus.  The blinking cursor is annoying!

        # Add bar container
        self.barContainer = Frame(self.frameProgress, bg="white", bd=2, relief=tk.SUNKEN)
        self.barContainer.place(relheight=0.12, relwidth=0.9, relx=0.05, rely=0.1)

        # Add bar and progress label
        self.prog = Label(self.barContainer, bg="orange")
        self.prog.place(x=0, relheight=1, relwidth = float(initProgress))
        
        self.lblProg = Label(self.frameProgress, bg="black", fg="white", justify="center", text=f"{initProgress}%")
        self.lblProg.place(x=0, rely=0.23, relwidth = 1)

        # Add status text


    def set_prog(self, x):
        """ Sets the progress bar's value.
            inputs:
                x - float between 0 and 1 representing % of progress
        """
        self.prog.place(x=0, relheight=1, relwidth=x)
        self.lblProg["text"] = f"{x}%"

    def set_status(self, text):
        """ Sets the status label to display input text """

        pass