# ------------------------------------------------------------------------------
# Main.py runs the project's GUI, allows the user to set the K value, run the
# IDW and regression analysis, and view the results.
# ------------------------------------------------------------------------------

import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as messagebox
from tkinter import ttk
from ProgressBar import ProgressBar
from time import sleep
from PIL import Image, ImageTk


root = tk.Tk()
root.title("GEOG 777 - Project 1 - Daniel Fourquet")
root.resizable(False, False)



# Background Image
BackgroundImg = ImageTk.PhotoImage(Image.open("backgroundInit.jpg"))
imgBackground = tk.Label(root, height=600, width=900, image=BackgroundImg)
imgBackground.pack()

# Results image
img = None

# Fonts
fontTitle = tkFont.Font(family="Oswald", size=20)
fontParagraph = tkFont.Font(family="Lucida Grande", size=12)
fontSmall = tkFont.Font(family="Lucida Grande", size=10)


def run_analysis(k):
    """ Runs the geoprocessing tools from RunAnalysis.py, generates
        output images via ArcGIS Pro, and displays the output in the
        results frame """
    
    
    # Validate K entry
    try:
        k = float(k)
        if k <= 1:
            raise ValueError
    
    except ValueError:
        messagebox.showerror("K Value Error", f"K = {k}\n\nInvalid K Value!  K must be a number greater than 1.")
        return

    # Run analysis
    btnRunAnalysis["state"] = "disabled"

    # Input data paths
    wells = "data/well_nitrate.shp"
    tracts = "data/cancer_tracts.shp"
    counties = "data/cancer_county.shp"

    # Show progress bar
    prog = ProgressBar(root)
    
    root.update()
    
    # Load arcpy - this is imported here to prevent waiting time when
    #              the program is first loaded
    prog.set_status("Loading arcpy...")
    prog.set_prog(0)
    import arcpy
    import RunAnalysis as ra
    import GenerateReports as gr

    prog.set_status("Preparing folder structure...")
    ra.initialize()

    prog.set_status(f"Interpolating nitrate levels from sample wells with IDW, K={k}...")
    prog.set_prog(0.25)
    idwOutput = ra.run_idw(wells, counties, k)

    prog.set_status("Summarizing results of the nitrate interpolation at the tract level...")
    prog.set_prog(0.3)
    nitrateVals = ra.get_average_nitrate_dict(tracts, "GEOID10", idwOutput, k)

    prog.set_status("Updating nitrates field in tracts...")
    prog.set_prog(0.5)
    ra.update_nitrates_field(nitrateVals, tracts)

    prog.set_status("Running ordinary least squares linear regression...")
    prog.set_prog(0.75)
    ra.run_ols(tracts, k)

    prog.set_status("Creating final maps...")
    prog.set_prog(0.90)
    gr.generate_reports(k)

    prog.set_status("Done!")
    prog.set_prog(1)
    sleep(2)
    
    prog.close()
    btnRunAnalysis["state"] = "active"

    show_frameResults(k)


def show_frameResults(k):
    """ Displays the results frame and updates the images with the latest
        analysis data """

    global img

    def load_image(k, type):     
        fileName = f'reports/{type}_{str(k).replace(".","_")}.jpg'
        print(fileName)
        img = Image.open(fileName)
        img = img.resize((353,457))
        imgTk = ImageTk.PhotoImage(img)
        return imgTk

    def change_image(k, type, curMap):
        imgTk = load_image(k, type)
        curMap.configure(image=imgTk)
        curMap.image = imgTk

    for child in frameResults.winfo_children():
        child.destroy()

    # Show frameResults
    frameResults.place(relheight=0.9, relwidth=0.4, relx=0.55, rely=0.05)

    # Show map image (default to IDW map)
    img = load_image(k, "IDW")
    curMap = tk.Label(frameResults, image=img)
    curMap.pack()

    # Show button controls
    frameButtons = tk.Frame(frameResults, bg="black", height=80) 
    frameButtons.pack(side='bottom', fill='x')

    btnIDW = ttk.Button(frameButtons, text="Show IDW Results", command=lambda: change_image(k, "IDW", curMap))
    btnIDW.pack()

    btnOLS = ttk.Button(frameButtons, text="Show OLS Results", command=lambda: change_image(k, "OLS", curMap))
    btnOLS.pack()
    







# Setup Frame
frameSetup = tk.Frame(root, bg="black", bd=5, relief=tk.RIDGE)
frameSetup.place(relheight=0.6, relwidth=0.35, relx=0.075, rely=0.05)

lblTitle = tk.Label(frameSetup,text="Nitrates and Cancer", fg="white", bg="black", justify="center", pady = 1, font=fontTitle)
lblTitle.place(x=0, y=0, relwidth=1, relheight=0.1)

lblDesc = tk.Label(frameSetup, anchor="n", text=open('projectDescription.txt').read(), fg="white", bg="black", pady = 2, justify="center", wraplength=250, font=fontParagraph)
lblDesc.place(x=0, rely=0.11, relwidth=1, relheight=0.3)

lblEnterK = tk.Label(frameSetup, text="Enter K value greater than 1 for IDW:", bg="black", fg="white", font=fontSmall)
lblEnterK.place(x=0, rely=0.61, relwidth=1)

frameKVal = tk.Frame(frameSetup, bg="black")
frameKVal.place(relx=0.2, rely=0.67, relwidth=0.6, relheight=0.1)

lblKEquals = tk.Label(frameKVal, text="K = ", bg="black", fg="white", font=fontSmall)
lblKEquals.pack(side="left")

txtKVal = tk.Entry(frameKVal)
txtKVal.insert(0, "1.2") # Set default value to 1.2
txtKVal.pack(side="left")

btnRunAnalysis = ttk.Button(frameSetup, text="Run Analysis", command=lambda: run_analysis(txtKVal.get()))
btnRunAnalysis.place(rely=0.83, relwidth=0.3, relx=0.35)



# Results Frame
frameResults = tk.Frame(root, bg="black", bd=5, relief=tk.RIDGE)


root.mainloop()