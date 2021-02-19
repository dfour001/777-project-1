# ------------------------------------------------------------------------------
# Main.py runs the project's GUI, allows the user to set the K value, run the
# IDW and regression analysis, and view the results.
# ------------------------------------------------------------------------------

import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()
canvas = tk.Canvas(root, height=600, width=900, bg="red")
canvas.pack()

# Background Image


# Fonts
fontTitle = tkFont.Font(family="Lucida Grande", size=20)
fontParagraph = tkFont.Font(family="Lucida Grande", size=12)

# Setup Frame
frameSetup = tk.Frame(root, bg="black", bd=10, relief=tk.RIDGE)
frameSetup.place(relheight=0.75, relwidth=0.35, relx=0.075, rely=0.05)

lblTitle = tk.Label(frameSetup,text="Nitrates and Cancer", fg="white", bg="black", justify="center", pady = 1, font=fontTitle)
lblTitle.place(x=0, y=0, relwidth=1, relheight=0.1)

lblDesc = tk.Label(frameSetup, anchor="n", text=open('projectDescription.txt').read(), fg="white", bg="black", pady = 2, justify="center", wraplength=250, font=fontParagraph)
lblDesc.place(x=0, rely=0.11, relwidth=1, relheight=0.2)

lblEnterK = tk.Label(frameSetup, text="Enter K value greater than 1 for IDW:", bg="black", fg="white", font=fontParagraph)
lblEnterK.place(x=0, rely=0.41, relwidth=1)

frameKVal = tk.Frame(frameSetup, bg="black")
frameKVal.place(x=20, rely=0.47, relwidth=0.8, relheight=0.1)

lblKEquals = tk.Label(frameKVal, text="K = ", bg="black", fg="white", font=fontParagraph)
lblKEquals.pack(side="left")

txtKVal = tk.Entry(frameKVal)
txtKVal.pack(side="left")




# Results Frame
frameResults = tk.Frame(root, bg="white")
frameResults.place(relheight=1, relwidth=0.5, relx=0.5)



root.mainloop()