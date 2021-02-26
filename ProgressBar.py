import tkinter as tk
from tkinter import Frame, Label
from PIL import Image, ImageTk

class ProgressBar(Frame):
    """ A custom widget based on the Frame class that displays a progress bar and status text """
    def __init__(self, root, initProgress = 0.75):
        super().__init__(root)

        self.backgroundImg = ImageTk.PhotoImage(Image.open("backgroundProgress.jpg"))
        self.backdrop = Label(root, image=self.backgroundImg)
        self.backdrop.place(x=0, y=0, relwidth=1, relheight=1)
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
        self.lblStatus = Label(self.frameProgress, bg="black", fg="white", justify="center")
        self.lblStatus.place(x=0, rely=0.57, relwidth=1)


    def set_prog(self, x):
        """ Sets the progress bar's value.
            inputs:
                x - float between 0 and 1 representing % of progress
        """
        self.prog.place(x=0, relheight=1, relwidth=x)
        self.lblProg["text"] = f"{int(x*100)}%"
        self.frameProgress.update()

    def set_status(self, text):
        """ Sets the status label to display input text """
        self.lblStatus["text"] = str(text)
        self.frameProgress.update()

    
    def close(self):
        """ Destroys the ProgressBar instance """
        self.frameProgress.destroy()
        self.backdrop.destroy()
        self.destroy()